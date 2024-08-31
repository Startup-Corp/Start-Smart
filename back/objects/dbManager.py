import os

from supabase import Client
from objects.supabase_init import supabase
import configparser

class DB_manager:
    def __init__(self):
        self.supabase: Client = supabase

    def insert(self, table: str, data: dict):
        request = self.supabase.table(table)

        if data is None:
            return "Data undefined"

        return request.insert([data]).execute()

    def select(self, table: str, columns="*", criteria=None):
        request = self.supabase.table(table).select(columns)

        if criteria is not None:
            for key, value in criteria.items():
                request = request.in_(key, value)

        return request.execute()

    def delete(self, table: str, criteria=None):
        request = self.supabase.table(table).delete()

        if criteria is not None:
            for key, value in criteria.items():
                if type(value) is list:
                    request = request.in_(key, value)
                else:
                    request = request.eq(key, value)

        return request.execute()


# url = config['supabase']['url']
# key = config['supabase']['key']
#
# print(url)
# print(key)
#
# db = DB_manager(url, key)
