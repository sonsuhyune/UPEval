import os
import re
import string
import random
from random import shuffle
import pickle
import json
import random
from prompt_template import PromptTemplate
# from dotenv import dotenv_values
from minutes_writer import *


def read_jsonl(file_path):
    print("================================")
    print(f"Loading data from {file_path}.")
    print("================================")

    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
        # data = data[0]['data']

    return data


def read_json(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        data = json.load(f)

    print("================================")
    print(f"Loading data from {file_path}.")
    print("================================")

    return data

def read_pkl(file_path):
    with open(file_path, 'rb') as f:
        data = pickle.load(f)

    print("================================")
    print(f"Loading data from {file_path}.")
    print("================================")

    return data

def save_json(obj, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

    print("================================")
    print(f"Saved at {file_path}.")


def api_setup(model):
    if "gpt" in model:
        with open("./openai_api_key.txt", 'r') as f:
            api_key = f.readline().strip()
    elif "gemini" in model:
        with open("./gemini_api_key.txt", 'r') as f:
            api_key = f.readline().strip()
    else:  # llama, mistral
        with open("./llama_api_key.txt", 'r') as f:
            api_key = f.readline().strip()

    return api_key


def normalize_text(text):
    def remove_articles(text):
        regex = re.compile(r"\b(a|an|the)\b", re.UNICODE)
        return re.sub(regex, " ", text)

    def white_space_fix(text):
        return " ".join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(text))))



def prompt_split_msg(input_prompt):
    system_prompt, user_prompt = input_prompt.split("---")[0], input_prompt.split("---")[-1]

    contents = dict()
    contents["system"] = system_prompt
    contents["user"] = user_prompt

    messages = [
        {"role": "system",
         "content": contents["system"]},
        {"role": "user",
         "content": contents["user"]}
    ]

    return messages


