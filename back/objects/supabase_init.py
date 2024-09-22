import os

from supabase import create_client, Client
from supabase.client import Client, ClientOptions
import configparser

from gotrue import SyncSupportedStorage
from flask import session

class FlaskSessionStorage(SyncSupportedStorage):
    def __init__(self):
        self.storage = session

    def get_item(self, key: str) -> str | None:
        if key in self.storage:
            return self.storage[key]

    def set_item(self, key: str, value: str) -> None:
        self.storage[key] = value

    def remove_item(self, key: str) -> None:
        if key in self.storage:
            self.storage.pop(key, None)


# print(os.getcwd())

config = configparser.ConfigParser()
config.read('./config.ini')

url: str = config['supabase']['url']
key: str = config['supabase']['key']
supabase: Client = create_client(url, key, options=ClientOptions(storage=FlaskSessionStorage()))
