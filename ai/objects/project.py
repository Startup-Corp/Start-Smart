from ai.objects.supabase_init import supabase
from storage3.utils import StorageException
import io
import os
import shutil
import zipfile


class GetProjectsByUserID:
    @staticmethod
    def execute(user_id: str):
        response = (
            supabase.table("Projects")
            .select("*")
            .eq("owner_id", user_id)
            .execute()
        )

        res = []
        for pr in response.data:
            res.append({
                'id': pr['id'],
                'name': pr['title'],
                'status': pr['status']
            })
        
        return res


class GetProjectImagesByID:
    @staticmethod
    def execute(project_id: int, owner_id: str, username: str):
        bucket_name = f'{username}_{str(owner_id)[:5]}'
        res = supabase.storage.from_(bucket_name).list(str(project_id))

        if len(res) == 0:
            return None
        
        data = io.BytesIO()
        with zipfile.ZipFile(data, mode='w') as z:
            for f in res:
                filename = f'{project_id}/{f["name"]}'
                filedata = supabase.storage.get_bucket(bucket_name).download(filename)
                z.writestr(f["name"], filedata)

        data.seek(0)
        
        return data


class GetProjectByID:
    @staticmethod
    def execute(project_id: int, user_id: str):
        response = (
            supabase.table("Projects")
            .select("*")
            .eq("owner_id", user_id)
            .eq("id", project_id)
            .execute()
        )

        project_data = response.data

        if len(project_data) == 0:
            return None

        project_data = project_data[0]

        del project_data['created_at']
        del project_data['owner_id']
        del project_data['bucket_id']
        
        return project_data
