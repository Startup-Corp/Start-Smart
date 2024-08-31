# from objects.dbManager import db as Connection
from objects.supabase_init import supabase
from flask import jsonify
#om storage3.utils import StorageException
# import io
# import zipfile
# import base64

class GetLastProjId:
    @staticmethod
    def execute(user_id: str):
        response = (
            supabase.table("Projects")
            .select("id")
            .eq("owner_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )

        if response.data:
            return response.data[0].get('id')
        else:
            return None


class GetBalanceByUserId:
    @staticmethod
    def execute(user_id: str):
        print(f'{user_id} and type {type(user_id)}')
        print(user_id == '02e46b95-b31f-43bf-81b2-02357ff83d8d')
        response = (
            supabase.table("meta_data")
            .select("*")
            # .eq("id", user_id)
            .execute()
        )
        print(response.data)
        if response.data:
            user_data = response.data[0]
            return user_data.get('ai_balance'), user_data.get('ex_balance')
        else:
            return None, None