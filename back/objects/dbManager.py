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

    def select(self, table: str, schema: str = "public", columns="*", criteria=None):
        request = self.supabase.schema(schema).table(table)

        if isinstance(columns, list) and columns != "*":
            request = request.select(','.join(columns))
        else:
            request = request.select(columns)

        if criteria is not None:
            for key, value in criteria.items():
                request = request.eq(key, value)

        response = request.execute()

        return response
    
    def delete(self, table: str, criteria=None):
        request = self.supabase.table(table).delete()

        if criteria is not None:
            for key, value in criteria.items():
                if type(value) is list:
                    request = request.in_(key, value)
                else:
                    request = request.eq(key, value)

        return request.execute()
