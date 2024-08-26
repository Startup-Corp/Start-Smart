from objects.dbManager import db as Connection
from objects.supabase_init import supabase
from storage3.utils import StorageException
import io
#import os
#import shutil
import zipfile
#import urllib.parse
import base64

class AddProject:
    def __init__(
            self,
            email: str,
            owner_id: str,
            title: str,
            description: str,
            funnel_desc: str,
            img_desc: str,
            metric_title: str,
            metric_desc: str,
            metric_target: str,
            extra_data: str,
            tariff: int,
            files: list) -> None:
        
        self.email = email
        self.owner_id = owner_id
        self.title = title
        self.description = description
        self.funnel_desc = funnel_desc
        self.img_desc = img_desc
        self.metric_title = metric_title
        self.metric_desc = metric_desc
        self.metric_target = metric_target
        self.extra_data = extra_data
        self.tariff = tariff
        self.files = files
    
    def _create_bucket(self):
        try:
            res = supabase.storage.create_bucket(f'{self.email}_{str(self.owner_id)[:5]}')
            print(res)
            return True
        except StorageException as ex:
            print(ex)
        except Exception as ex:
            print(ex)
        return False

    def _get_bucket_info(self):
        try:
            res = supabase.storage.get_bucket(f'{self.email}_{str(self.owner_id)[:5]}')
            return res
        except StorageException as ex:
            print(ex)
        except Exception as ex:
            print(ex)
        return None

    def _get_bucket_id(self):
        bucket_info = self._get_bucket_info()
        if bucket_info is None:
            if self._create_bucket() is False:
                assert AssertionError("Can't create bucket")
            bucket_info = self._get_bucket_info()

        return bucket_info.id

    def _add_project_data(self, bucket_id: str):
        res = (supabase.table('Projects').insert({
            'owner_id': self.owner_id,
            'title': self.title,
            'description': self.description,
            'funnel_desc': self.funnel_desc,
            'img_desc': self.img_desc,
            'metric_title': self.metric_title,
            'metric_desc': self.metric_desc,
            'metric_target': self.metric_target,
            'extra_data': self.extra_data,
            'tariff': self.tariff,
            'bucket_id': bucket_id
        }).execute())
        print(res)
        return res.data[0]['id']
        

    def _upload_images(self, bucket_id: str, project_id: int):
        files = self.files

        for f in files:
            encoded_filename = base64.urlsafe_b64encode(f.filename.encode()).decode()

            file_data = f.read()
            
            if not file_data:
                print(f"File {f.filename} is empty or could not be read")
                continue
            
            response = supabase.storage.from_(f'{self.email}_{str(self.owner_id)[:5]}').upload(
                file=file_data,
                path=f'/{project_id}/{encoded_filename}',
                file_options={"content-type": f.content_type}
            )

            # Логирование результата для отладки
            print(f"Uploaded {f.filename} as {encoded_filename} with response: {response}")


    def execute(self):
        
        try:
            bucket_id = self._get_bucket_id()
        except Exception as ex:
            print(ex)
            return
        
        project_id = self._add_project_data(bucket_id)

        self._upload_images(bucket_id, project_id)
        

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
    def execute(project_id: int, owner_id: str, email: str):
        bucket_name = f'{email}_{str(owner_id)[:5]}'
        res = supabase.storage.from_(bucket_name).list(str(project_id))

        if len(res) == 0:
            return None
        
        data = io.BytesIO()
        with zipfile.ZipFile(data, mode='w') as z:
            for f in res:
                decoded_filename = base64.urlsafe_b64decode(f["name"]).decode('utf-8')
                
                filename = f'{project_id}/{f["name"]}'
                filedata = supabase.storage.get_bucket(bucket_name).download(filename)
                
                z.writestr(decoded_filename, filedata)

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
