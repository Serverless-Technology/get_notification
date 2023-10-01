import os
import time

from datetime import datetime
from src.storage.aws_storage import AmazonWebStorage


def create_dir(dir_path: str):
    os.makedirs(dir_path, exist_ok=True)


def get_storage_instance(path: str):
    return AmazonWebStorage(src_path=path)


def upload_log(response: dict, log_path: str):
    pass


def save_response(response: dict):
    pass


def upload_event(storage, src_path, dst_path, max_attempts):
    is_uploaded = False

    for i in range(max_attempts):
        try:
            storage.upload(src_path, dst_path)
            is_uploaded = True
            break
        except Exception as e:
            print(f"Error while uploading event : {src_path}")
            print(e)
            time.sleep(10)

            continue

    if not is_uploaded:
        raise Exception(f"Failed to upload event : {src_path} to {dst_path}")