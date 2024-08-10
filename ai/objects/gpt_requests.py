from ai.objects.supabase_init import supabase

class AddRequest:
    @staticmethod
    def execute(project_id: str, input_tokens: int, output_tokens: int, output_txt: str, type: int):
        res = (supabase.table('GPT_requests').insert({
            'project_id': project_id,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'output_txt': output_txt,
            'type': type
        }).execute())
        
        return res