import sys
from typing import List

from minio import Minio
from io import BytesIO

from models import MemStorage


class FileStorage:
    def __init__(self, url, access_key, secret_key, bucket, secure=False):

        self.client = Minio(url,
                            access_key,
                            secret_key,
                            secure=secure)
        self.bucket = bucket

    async def list_objects(self) -> List[str]:
        _list = list(self.client.list_objects(self.bucket))
        return _list


    def check_bucket(self):
        if self.client.bucket_exists(self.bucket):
            print(f"Bucket exists: {self.bucket}")
        else:
            self.client.make_bucket(f"bucket created: {self.bucket}")

    async def upload_file(self, filename: str, data: BytesIO, length: int) \
            -> None:
        self.client.put_object(self.bucket, object_name=filename,
                               length=length, data=data)
        return

    def delete_file(self, filename: str):
        self.client.remove_object(self.bucket, filename)

    def download_file(self, filename: str) -> str:
        return self.client.get_presigned_url(method="GET",
                                             object_name=filename,
                                             bucket_name=self.bucket)


storage = FileStorage("127.0.0.1:9000", 'YtbcKEKGO4vLHdv6W6zk',
                      'Zc1UTPFx6kRrSNJgo1Dfz0i9v5lU4ujSQoWNlzWJ', 'test')

