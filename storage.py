from typing import List
from minio import Minio
from io import BytesIO


# class represents main actions with Minio storage
class FileStorage:
    def __init__(self, url, access_key, secret_key, bucket, secure=False):

        self.client = Minio(url,
                            access_key,
                            secret_key,
                            secure=secure)
        self.bucket = bucket

    # returns list of all objects in the storage
    async def list_objects(self) -> List[str]:
        _list = list(self.client.list_objects(self.bucket))
        return _list

    # checking if bucket exists, otherwise creating it
    def check_bucket(self) -> str:
        if self.client.bucket_exists(self.bucket):
            print('ok')
            return f"Bucket exists: {self.bucket}"
        else:
            self.client.make_bucket(f"bucket created: {self.bucket}")

    # uploading file to the storage
    async def upload_file(self, filename: str, data: BytesIO, length: int) \
            -> None:
        self.client.put_object(self.bucket, object_name=filename,
                               length=length, data=data)
        return

    # deleting file
    def delete_file(self, filename: str):
        self.client.remove_object(self.bucket, filename)

    # obtaining link to download file
    def download_file(self, filename: str) -> str:
        return self.client.get_presigned_url(method="GET",
                                             object_name=filename,
                                             bucket_name=self.bucket)


# an instance to connect to the storage
storage = FileStorage("127.0.0.1:9000", 'niCT17yEjaM9HwWcjvEo',
                      'QL1gNwiZY8kaGPOfYki9i82f043wboTjqR1DSc94', 'memes')


