import os
import json
import shutil
from datetime import date
from serpapi import GoogleSearch
# from config import SRC_PATH, DEST_PATH
from src.storage.upload_model import get_storage_instance, upload_event
from dotenv import load_dotenv

load_dotenv()

SRC_PATH = os.environ.get("SRC_PATH")
DEST_PATH = os.environ.get("DEST_PATH")

def upload_to_bucket(count, event, tag, user_email):
    storage = get_storage_instance(path=f"{DEST_PATH}")
    count = count + 1
    today=date.today()
    file_name = f"./events/{tag}/{today}_{count}"
    with open(f"{file_name}.json", "w", encoding="utf-8") as json_file:
        json.dump(event, json_file, ensure_ascii=False, indent=4)

    dst_path = f"{DEST_PATH}/{user_email}/{tag}/{today}_{count}.json"
    src_path = f"{SRC_PATH}/{tag}/{today}_{count}.json"
    upload_event(storage, src_path, dst_path, max_attempts=3)
    # print(f"Removing file {file_name}.json from local Events directory")
    # os.remove(f"{file_name}.json")


def fetch_google_data(tag, user_email):
    DIR_PATH = f"./events/{tag}"
    params = {
        "engine": "google_events",
        "q": tag,
        "hl": "en",
        "gl": "us",
        "api_key": "f5bca446203ba13b76ece776baef70e7da283e15fa26f3e612c12303c658b58c",
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        events_results = results["events_results"]
    except Exception as e:
        print(f"Error occured while fetching data: {e}")
        return

    if not os.path.exists(DIR_PATH):
        print("Directory does not exist, creating directory...")
        os.makedirs(DIR_PATH)
    else:
        print(
            "Directory already exists, removing all files and recreating the directory..."
        )
        shutil.rmtree(DIR_PATH)
        os.makedirs(DIR_PATH)

    for count, event in enumerate(events_results):
        # save_file(count, event, DIR_PATH)
        upload_to_bucket(count, event, tag, user_email)
    # os.rmdir(DIR_PATH)
