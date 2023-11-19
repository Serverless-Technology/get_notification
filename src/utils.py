import os
from dotenv import load_dotenv
import json


from src.storage.upload_model import get_storage_instance, upload_event


load_dotenv()

SRC_PATH = os.environ.get("SRC_PATH")
DEST_PATH = os.environ.get("DEST_PATH")

def upload_to_bucket(event):
    storage = get_storage_instance(path=f"{DEST_PATH}")
    file_name = f"{event['Event Name']}"
    with open(f"events/{file_name}.json", "w", encoding="utf-8") as json_file:
        json.dump(event, json_file, ensure_ascii=False, indent=4)

    dst_path = f"{DEST_PATH}/{file_name}.json"
    src_path = f"{SRC_PATH}/{file_name}.json"
    upload_event(storage, src_path, dst_path, max_attempts=3)
    print(f"Removing file {file_name}.json from local Events directory")
    os.remove(src_path)