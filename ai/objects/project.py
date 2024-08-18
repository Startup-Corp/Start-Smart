from ai.objects.supabase_init import supabase


class UploadReport:
    @staticmethod
    def execute(bucket_id: str, project_id: int, file: bytes):
        supabase.storage.from_(bucket_id).upload(
            file=file, 
            path=f'/{project_id}/result.md',
            file_options={
                "content-type": 'text/markdown',
                'upsert': 'true'
            })


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
        
        files = []
        for f in res:
            if '.png' not in f['name'] and '.jpg' not in f['name']:
                continue
            
            filename = f'{project_id}/{f["name"]}'
            filedata = supabase.storage.get_bucket(bucket_name).download(filename)
            files.append(filedata)
        
        return files


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
