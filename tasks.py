import os
import math
from collections import Counter
from evaluate import load
from utils import *


class Generator:
    def __init__(self, writer, prompt_template, prompt_type):
        self.writer = writer
        print(self.writer.model)
        self.prompt = prompt_template
        self.prompt_type = prompt_type

    def parse_data(self, datum, exemplar, speaker, checkresult=None):

        role_info = datum['role']
        conversation_history = datum['history']

        if "user" == speaker:
            prompt = self.prompt.prompting(**{'role_card': role_info,
                                              'conversation_history': conversation_history,
                                              })

        elif "supporter" == speaker:
            prompt = self.prompt.supporter_prompting(**{'role_card': role_info,
                                                        'conversation_history': conversation_history,
                                                        })
        elif "self-check" == speaker:
            conversation_history = datum['history'][-2:] ###### 여기 task.py line 31


            prompt = self.prompt.checker_prompting(**{'role_card': role_info,
                                                  'conversation_history': conversation_history,
                                                  })
        elif "repeat" == speaker:
            conversation_history = datum['history'] ###### 여기 task.py line 31
            print("*"*30)
            print(conversation_history)

            prompt = self.prompt.repeat_prompting(**{'role_card': role_info,
                                                  'conversation_history': conversation_history,
                                                  })
        elif "scoring" == speaker:
            conversation_history = datum['history'][-2:]


            prompt = self.prompt.scoring_prompting(**{'role_card': role_info,
                                                  'conversation_history': conversation_history,
                                                  'Q1_answer': checkresult["Q1"],
                                                  'Q2_answer': checkresult["Q2"],
                                                  'Q3_answer': checkresult["Q3"],
                                                  'Q4_answer': checkresult["Q4"],
                                                  'Q5_answer': checkresult["Q5"],
                                                  'Q6_answer': checkresult["Q6"],
                                                  'Q7_answer': checkresult["Q7"],

                                                  })
        elif "repeat_score" == speaker:

            conversation_history = datum['history']


            prompt = self.prompt.repeat_score_prompting(**{'role_card': role_info,
                                                  'conversation_history': conversation_history,
                                                  'Q1': checkresult["Q1"],

                                                  })
            # print(prompt)
        elif "repeat_score_only" == speaker:

            conversation_history = datum['history']


            prompt = self.prompt.repeat_score_only_prompting(**{'role_card': role_info,
                                                  'conversation_history': conversation_history,


                                                  })
            # print(prompt)

        system_prompt, user_prompt = prompt.split("---")[0], prompt.split("---")[-1]

        contents = dict()
        contents["system"] = system_prompt
        contents["user"] = user_prompt

        return contents

    def r_generate(self, contents, model_type, speaker_type, type=None):
        if type == "supporter":
            messages = [
                {"role": "system",
                 "content": contents["system"]},
                {"role": "assistant",
                 "content": contents["user"]}
            ]
            print("assistant")
        else:
            messages = [
                {"role": "system",
                 "content": contents["system"]},
                {"role": "user",
                 "content": contents["user"]}
            ]
        if "gpt" in model_type:
            if speaker_type == "scoring":
                print("scoring  "*30)
                response = self.writer.write_score(messages)

            else:
                response = self.writer.write(messages)
        elif "llama" in model_type or "mistral" in model_type or "gemma" in model_type:
            response = self.writer.llama_write(messages)
        else:  # gemini
            response = ""



        return response

