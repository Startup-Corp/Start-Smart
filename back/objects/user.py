from objects.supabase_init import supabase

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
        response = (
            supabase.table("meta_data")
            .select("ai_balance, ex_balance")
            .eq("id", user_id)
            .execute()
        )

        if response.data:
            user_data = response.data[0]
            return user_data.get('ai_balance'), user_data.get('ex_balance')
        else:
            return None, None
        

class DecUserBalanceByUserId:
    @staticmethod
    def execute(user_id: str, tariff: int):
        response = (
            supabase.table("meta_data")
            .select("ai_balance, ex_balance")
            .eq("id", user_id)
            .execute()
        )

        if not response.data:
            raise ValueError(f'No tariff for user: {user_id}')
        
        user_data = response.data[0]
        ai_balance, ex_balance = user_data.get('ai_balance'), user_data.get('ex_balance')

        if tariff == 1: # ai
            _ = (
                supabase.table("meta_data")
                .update({"ai_balance": ai_balance-1})
                .eq("id", user_id)
                .execute()
            )
        else:
            _ = (
                supabase.table("meta_data")
                .update({"ex_balance": ex_balance-1})
                .eq("id", user_id)
                .execute()
            )
