import os
import json
import shutil
from serpapi import GoogleSearch
import sys
from src.storage.upload_model import get_storage_instance, upload_event
from config_ import SRC_PATH, DEST_PATH

from datetime import datetime


params = {
  "engine": "google_events",
  "q": "International Conferences",
  "hl": "en",
  "gl": "us",
  "api_key": "f5bca446203ba13b76ece776baef70e7da283e15fa26f3e612c12303c658b58c"
}

try:
    search = GoogleSearch(params)
    results = search.get_dict()
    events_results = results["events_results"]
except Exception as e:
    print(e)

if not os.path.exists("./src/google-search/events"):
    os.makedirs("./src/google-search/events")
else :
    print("Directory already exists, removing all files and recreating the directory...")
    shutil.rmtree("./src/google-search/events")
    os.makedirs("./src/google-search/events")
    

def upload_to_bucket(count, event):
    count=count+1
    file_name=f"./src/google-search/events/{count}"
    with open(f'{file_name}.json', 'w', encoding='utf-8') as json_file:
        json.dump(event, json_file, ensure_ascii=False, indent=4)
    day=datetime.now().strftime("%Y_%m_%d")
    time=datetime.now().strftime("%Y_%m_%d_T%H%M")
    dst_path=f"{DEST_PATH}{day}/{time}/{count}.json"
    src_path=f"{SRC_PATH}/{count}.json"
    upload_event(storage, src_path, dst_path, max_attempts=3)

storage=get_storage_instance(path=f"{DEST_PATH}")
for count, event in enumerate(events_results):
    upload_to_bucket(count, event)