from openai import OpenAI
import tiktoken
import configparser
import httpx
import logging
from pprint import pprint

config = configparser.ConfigParser()
config.read('config.ini')

class Assistent:
    def __init__(self, key, proxy=None):
        self.client = OpenAI(api_key=key, http_client=proxy)

    def _get_model_list(self):
        models = self.client.models.list()
        return models

    def _num_tokens_from_string(self, string: str, encoding_name: str) -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.encoding_for_model(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def _num_tokens_from_messages(self, messages, model):
        """Return the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        
        tokens_per_message = 3
        tokens_per_name = 1
        
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

    def create_request(self, messages: list, model = "gpt-4o-mini"):
        self._validate_messages(messages)
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages)
        input_tokens = completion.usage.prompt_tokens
        output_tokens = completion.usage.completion_tokens
        
        return completion.choices[0].message.content, input_tokens, output_tokens

if __name__ == '__main__':
    proxies = {"http://": config['openai']['proxy_addr'], "https://": config['openai']['proxy_addr']}
    http_client = httpx.Client(proxies=proxies)

    a = Assistent(config['openai']['api_key'], http_client)
    print(a._get_model_list())
    print(tiktoken.list_encoding_names())
    print(tiktoken.encoding_for_model("gpt-4o-mini") )
    messages = [
        {'role': 'system', 'content': 'You are aboba'},
        {'role': 'user', 'content': 'Hello'}
    ]
    pprint(a.create_request(messages))