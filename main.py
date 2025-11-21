# import pandas as pd
import numpy as np
import json
import os
import copy
import sys
import argparse
from minutes_writer import MinuteWriter
from utils import *
from tasks import *
from prompt_template import PromptTemplate
from datetime import datetime
from tqdm import tqdm
import random
from random import shuffle
import re
import ast

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # parser.add_argument("--task", default="gen", type=str, required=True)  # gen, data_const, eval
    parser.add_argument("--model_type", default="chatgpt", type=str, required=True)
    parser.add_argument("--input_path", default="", type=str)
    parser.add_argument("--output_path", default="", type=str)
    parser.add_argument("--prompt", default="upeval", type=str)
    parser.add_argument("--data_type", default="trivia", type=str)
    parser.add_argument("--api_key", default="your api key", type=str)
    parser.add_argument("--start_idx", default=0, type=int)
    parser.add_argument("--end_idx", default=0, type=int)
    parser.add_argument("--eval_turn", default=10, type=int)
    parser.add_argument("--check_turn", default=2, type=int)

    args = parser.parse_args()



    # >>> file path setup
    if args.input_path != None and args.output_path != None:
        input_path = args.input_path

        output_dir, output_file = "/".join(args.output_path.split("/")[:-1]), args.output_path.split("/")[-1]
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir, output_file)

    else:
        raise ValueError("Check the data_type")


    data = read_json(input_path)

    ### For debug
    if args.start_idx != 0 and args.end_idx != 0:
        data = data[args.start_idx:args.end_idx]
    else:
        if args.start_idx != 0:
            data = data[args.start_idx:]
        if args.end_idx != 0:
            data = data[:args.end_idx]


    # >>> model + prompt setup
    # if 'gen' in args.task:

        # writer setup

    api_key = args.api_key
    Writer = MinuteWriter(api_key, args.model_type)
    prompt_template = PromptTemplate(args.prompt)
    pred_model = Generator(Writer, prompt_template, args.prompt)

    Writer_S = MinuteWriter(api_key, args.model_type)
    pred_model_S = Generator(Writer_S, prompt_template, args.prompt)

    if 'icl' in args.prompt:
        # static num_shot -> 1
        num_shot = 1
        # exemplar = get_exemplars(num_shot)[0]
    else:  # vanilla, cot ...
        exemplar = ""

    new_data = []
    data_idx = 0
    error_count =0
    total_count =0
    print(len(data))
    for datum in tqdm(data):

        datum['history'] = []

        datum['self-check'] = {}
        if len(datum["dialog"]) < 4:
            continue
        inputs = datum["dialog"][3]["input"].split("\n")
        inputs = inputs[:-1]
        gold = datum["dialog"][3]["gold"]
        datum['history'].extend(inputs)


        if "upeval" in args.prompt:
            for i in range(args.eval_turn):


                speaker_type = "supporter"
                contents = pred_model.parse_data(datum, exemplar, speaker_type)
                response = pred_model.r_generate(contents, args.model_type, speaker_type, type="supporter")


                # datum["dialog"].append({"input": datum['history'], "generated_utt":response[0], "gold":d})
                datum['history'].append(f"supporter: {response[0]}")

                print(f"speaker: {speaker_type}, response: {response}")
                sup_response = response[0]

                speaker_type = "user"
                contents = pred_model.parse_data(datum, exemplar, speaker_type)
                response = pred_model.r_generate(contents, args.model_type, speaker_type)
                datum['history'].append(f"help-seeker: {response[0]}")

                print(f"speaker: {speaker_type}, response: {response}")

                # exit(0) speaker_type}, response: {response



                if (i+1) % args.check_turn == 0:
                    speaker_type = "self-check"
                    contents = pred_model.parse_data(datum, exemplar, speaker_type)
                    response = pred_model.r_generate(contents, args.model_type, speaker_type)
                    tmp = {}
                    tmp["dialog_id"] = f"{data_idx}_{i}"
                    tmp["history"] =  copy.deepcopy(datum['history'])

                    total_count+=1
                    # breakpoint()
                    check_response = response[0]
                    check_response = check_response.replace("[Start of Output]\n", "")
                    check_response = check_response.replace("\n[End of Output]", "")
                    check_result = ""
                    try:
                        cleaned_text = check_response.encode().decode('unicode_escape')  # \n, \' 등 실제 문자로 변환
                        cleaned_text = re.search(r'\{.*\}', cleaned_text, re.DOTALL).group(0)

                        parsed_dict = json.loads(cleaned_text)
                        check_result = parsed_dict
                        tmp["self-check-results"] = parsed_dict
                    except Exception as  e:
                        try:
                            print("*"*30, "JSONDecodeError:", e)

                            import re

                            text = check_response

                            pattern = re.compile(r"(Q[1-8]): (.*?)(?=\nQ[1-8]: |\Z)", re.DOTALL)
                            matches = pattern.findall(text)

                            result = {key: value.strip() for key, value in matches}

                            check_result = result
                            tmp["self-check-results"] = check_result
                            error_count+=1
                            if check_result == {}:
                                check_result = ast.literal_eval(check_response)
                                tmp["self-check-results"] = check_result
                        except Exception as e2:
                            tmp["self-check-results"] = {"error_idx": datum["dialog_id"], "error_response":check_response}
                            print("*" * 30, "JSONDecodeError:", e2)


                    speaker_type = "scoring"
                    print("&"*30)
                    print(check_result)
                    print("&" * 30)
                    contents = pred_model.parse_data(datum, exemplar, speaker_type, checkresult=check_result)
                    checker_response = pred_model.r_generate(contents, args.model_type, speaker_type)
                    checker_response = checker_response[0]
                    checker_response = checker_response.replace("[Start of Output]\n", "")
                    checker_response = checker_response.replace("\n[End of Output]", "")
                    checker_response = checker_response.replace("```", "")
                    checker_response = checker_response.replace("json", "")

                    tmp["self-check-results-score"] = json.loads(checker_response)





                    datum['self-check'][i] =  tmp


                if args.eval_turn -1 == i:
                    speaker_type = "repeat"
                    repeat_response = ""
                    repeat_score_response_ = ""

                    repeat_contents = pred_model.parse_data(datum, exemplar, speaker_type)
                    repeat_response = pred_model.r_generate(repeat_contents, args.model_type, speaker_type)
                    repeat_result = repeat_response[0]
                    repeat_result = repeat_result.replace("[Start of Output]\n", "")
                    repeat_result = repeat_result.replace("\n[End of Output]", "")
                    repeat_result = json.loads(repeat_result)

                    repeat_score_contents = pred_model.parse_data(datum, exemplar, "repeat_score", checkresult=repeat_result)
                    repeat_score_response_ = pred_model.r_generate(repeat_score_contents, args.model_type, "repeat_score")
                    repeat_score_response = repeat_score_response_[0]
                    repeat_score_response = repeat_score_response.replace("[Start of Output]\n", "")
                    repeat_score_response = repeat_score_response.replace("\n[End of Output]", "")
                    repeat_score_response = repeat_score_response.replace("```", "")
                    repeat_score_response = repeat_score_response.replace("json", "")

                    repeat_score_response = json.loads(repeat_score_response)






                    datum['self-check']["repeat"] = {"repeat-checker-results": repeat_result,
                                                     "repeat-checker-results-score":repeat_score_response}








            del datum["dialog"]

        data_idx += 1


        new_data.append(datum)
        save_json(new_data, output_path)



