import os
import boto3
from botocore.exceptions import ClientError
from copy import copy

from .base import Storage
from dotenv import load_dotenv

load_dotenv()
# from config import AWS_ACCESSS_KEY, AWS_ACCESS_SECRET

AWS_ACCESSS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_ACCESS_SECRET = os.environ.get("AWS_ACCESS_SECRET")
class AmazonWebStorage(Storage):
    def __init__(
        self,
        src_path,
        access_key_id=AWS_ACCESSS_KEY,
        secret_access_key=AWS_ACCESS_SECRET,
    ):
        self.resource, self.client = self.authenticate_client(
            access_key_id, secret_access_key
        )
        self.bucket = self.get_storage_bucket(src_path)

    def authenticate_client(self, access_key_id, secret_access_key):
        session = boto3.Session(access_key_id, secret_access_key)
        s3_resource = session.resource("s3")
        s3_client = session.client("s3")
        return s3_resource, s3_client

    def get_storage_bucket(self, src_path):
        print("src_path= ", src_path)
        bucket_name = src_path.split("/")[2]
        return self.resource.Bucket(bucket_name)

    def download(self, src_path, dst_path):
        pass

    def copy(self, src_path, dst_path):
        pass

    def upload(self, src_path, dst_path):
        s3_dst_path = copy(dst_path).replace(f"s3://{self.bucket.name}/", "")
        cog_exists = self.validate(s3_dst_path)
        if cog_exists:
            print(f"File already present in path: {dst_path}")
            exit(1)
        else:
            try:
                print("\n Trying to upload file... \n ")
                self.client.upload_file(src_path, self.bucket.name, s3_dst_path)
            except ClientError as e:
                print(f"Upload failed: src :{src_path}, dst:{dst_path}")
                exit(1)
            print(f"{src_path} uploaded to {dst_path}")

    def validate(self, path):
        try:
            self.resource.Object(self.bucket.name, path).load()
        except ClientError as e:
            return False
        else:
            return True
