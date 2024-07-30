from openai import OpenAI
import tiktoken
import configparser
import logging
from pprint import pprint

config = configparser.ConfigParser()
config.read('../config.ini')

class Assistent:
    def __init__(self, key):
        self.client = OpenAI(api_key=key)

    def _num_tokens_from_string(self, string: str, encoding_name: str) -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.encoding_for_model(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def _num_tokens_from_messages(self, messages, model="gpt-3.5-turbo"):
        """Return the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        if model in {
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k-0613",
            "gpt-4-0314",
            "gpt-4-32k-0314",
            "gpt-4-0613",
            "gpt-4-32k-0613",
            }:
            tokens_per_message = 3
            tokens_per_name = 1
        elif model == "gpt-3.5-turbo-0301":
            tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
            tokens_per_name = -1  # if there's a name, the role is omitted
        elif "gpt-3.5-turbo" in model:
            print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
            return self._num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
        elif "gpt-4" in model:
            print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
            return self._num_tokens_from_messages(messages, model="gpt-4-0613")
        else:
            raise NotImplementedError(
                f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
            )
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens

    def _validate_messages(self, messages: list):
        for message in messages:
            if 'role' not in message or \
                'content' not in message:
                raise ValueError('Not valid messages')

    def create_request(self, messages: list, model = "gpt-3.5-turbo"):
        num_of_tokens = self._num_tokens_from_messages(messages, model)
        print(num_of_tokens)
        self._validate_messages(messages)
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages)
        return completion.choices[0].message.content

# if __name__ == '__main__':
#     a = Assistent(config['openai']['api_key'])
#     messages = [
#         {'role': 'system', 'content': 'You are aboba'},
#         {'role': 'user', 'content': 'Hello'}
#     ]
#     pprint(a.create_request(messages))