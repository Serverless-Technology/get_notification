import os
import json
import shutil
from serpapi import GoogleSearch

TAG = "ICC Matches"

def save_file(count, event, dir_path):
    count=count+1
    file_name=f"{dir_path}/{count}"
    with open(f'{file_name}.json', 'w', encoding='utf-8') as json_file:
        print(f"Saving file {file_name}.json")
        json.dump(event, json_file, ensure_ascii=False, indent=4)

def fetch_google_data(tag):
    DIR_PATH = f"./src/google_events/events/{tag}"
    params = {
    "engine": "google_events",
    "q": tag,
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

    if not os.path.exists(DIR_PATH):
        print("Directory does not exist, creating directory...")
        os.makedirs(DIR_PATH)
    else :
        print("Directory already exists, removing all files and recreating the directory...")
        shutil.rmtree(DIR_PATH)
        os.makedirs(DIR_PATH)
    
    for count, event in enumerate(events_results):
        save_file(count, event, DIR_PATH)

fetch_google_data(TAG)
