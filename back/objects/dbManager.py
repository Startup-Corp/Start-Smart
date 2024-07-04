import supabase
from supabase import create_client, Client


class DB_manager:
    def __init__(self, supabase_url, supabase_key):
        self.supabase: Client = create_client(supabase_url, supabase_key)

    def insert(self, table: str, data: dict):
        request = self.supabase.table(table)

        if data is None:
            return "Data undefined"

        return request.insert([data]).execute()

    def select(self, table: str, columns="*", criteria=None):
        request = self.supabase.table(table).select(columns)

        if criteria is not None:
            request = request.in_(criteria.keys()[0], [criteria[criteria.keys()[0]]])

        return request.execute()

    def delete(self, table: str, criteria=None):
        request = self.supabase.table(table).delete()

        if (type(criteria[criteria.keys()[0]]) == list):
            request = request.in_(criteria.keys()[0], criteria[criteria.keys()[0]])
        else:
            request = request.eq(criteria.keys()[0], criteria[criteria.keys()[0]])

        return request.execute()