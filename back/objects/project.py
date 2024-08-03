from objects.dbManager import db as Connection
from objects.supabase_init import supabase
from storage3.utils import StorageException

class AddProject:
    def __init__(
            self,
            username: str,
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
        
        self.username = username
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
            res = supabase.storage.create_bucket(f'{self.username}_{str(self.owner_id)[:5]}')
            return True
        except StorageException as ex:
            print(ex)
        except Exception as ex:
            print(ex)
        return False

    def _get_bucket_info(self):
        try:
            res = supabase.storage.get_bucket(f'{self.username}_{str(self.owner_id)[:5]}')
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

        print(files)

        for f in files:
            supabase.storage.from_(f'{self.username}_{str(self.owner_id)[:5]}').upload(file=f.read(), path=f'/{project_id}/{f.filename}', file_options={"content-type": f.content_type})


    def execute(self):
        
        try:
            bucket_id = self._get_bucket_id()
        except Exception as ex:
            print(ex)
            return
        
        project_id = self._add_project_data(bucket_id)

        self._upload_images(bucket_id, project_id)
        