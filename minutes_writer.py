import json
import time
import openai
from prompt_template import PromptTemplate


class MinuteWriter:
    def __init__(self, api_key, model_type):
        self.model_type = model_type
        if 'chatgpt' in model_type or "gpt-3.5" in model_type:
            openai.api_key = api_key
            self.model = "gpt-3.5-turbo-0125"
        elif 'gpt4' in model_type or 'gpt-4' in model_type:  # for gen & input corruption
            openai.api_key = api_key
            # self.model = "gpt-4o-mini-2024-07-18"
            self.model = "gpt-4o-2024-08-06"
        elif 'claude' in model_type:
            pass




    def write(self, messages, reasoning_path=None, typ=None):
        # multi-step prompts


        print("================================")
        print("Msg for API: ")
        print(messages)
        print()


        results = []
        retries = 0
        while 5:
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    temperature=0.75,
                    top_p=0.9,
                    messages=messages,
                    # max_tokens=
                )
                result = response['choices'][0]['message']['content']
                results.append(result)
                print(results)

                return results
            except:
                retries += 1
                print(f"Request failed. Retrying ({retries} …")
                time.sleep(2 * retries)


    def write_score(self, messages, reasoning_path=None, typ=None):
        # multi-step prompts
        if typ is not None:
            print("================================")
            print(f"Prompt type: {typ}")
            print()
        else:
            print("================================")
            print("Prompt type: Vanilla")
            print()

        print("================================")
        print("Msg for API: ")
        print(messages)
        print()


        results = []
        retries = 0
        while 5:
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    temperature=0,
                    top_p=0.7,
                    messages=messages,
                    # max_tokens=
                )
                result = response['choices'][0]['message']['content']
                results.append(result)
                print(results)

                return results
            except:
                retries += 1
                print(f"Request failed. Retrying ({retries} …")
                time.sleep(2 * retries)
