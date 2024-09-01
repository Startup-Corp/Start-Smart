from objects.supabase_init import supabase
import logging
import base64


STATUS_ID = {
    'Create': 0,
    'AI': 1,
    'Human': 2,
    'Done': 3
}

class UploadReport:
    @staticmethod
    def execute(bucket_id: str, project_id: int, file: bytes, filename: str = 'result.md'):
        logging.info(f'Upload report. pr_id: {project_id}, bucket: {bucket_id}')
        encoded_filename = base64.urlsafe_b64encode(filename.encode()).decode()
        supabase.storage.from_(bucket_id).upload(
            file=file, 
            path=f'/{project_id}/{encoded_filename}',
            file_options={
                "content-type": 'text/markdown',
                'upsert': 'true'
            })


class UpdateVerified:
    @staticmethod
    def execute(project_id: int, verified: bool = True):
        logging.info(f'UpdateVerified. pr_id: {project_id}, verified: {verified}')
        response = (
            supabase.table("Projects")
            .update({"verified": verified})
            .eq("id", project_id)
            .execute()
        )


class UpdateProjectStatus:
    @staticmethod
    def execute(project_id: int, status: str):
        logging.info(f'UpdateProjectStatus. pr_id: {project_id}, status: {status}')
        if status not in STATUS_ID.keys():
            logging.error(f'Unknown pr status: {status}')
            return
        response = (
            supabase.table("Projects")
            .update({"status": STATUS_ID[status]})
            .eq("id", project_id)
            .execute()
        )


class GetProjectsByUserID:
    @staticmethod
    def execute(user_id: str):
        logging.info(f'GetProjectsByUserID. user_id: {user_id}')
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
        logging.info(f'GetProjectImagesByID. user_id: {owner_id}, pr_id: {project_id}, username: {username}')
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
        logging.info(f'GetProjectImagesByID. user_id: {user_id}, pr_id: {project_id}')
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
