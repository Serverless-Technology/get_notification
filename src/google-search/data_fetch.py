import os
import json
import shutil
from serpapi import GoogleSearch


params = {
  "engine": "google_events",
  "q": "Research Conferences in India",
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

if not os.path.exists("events"):
    os.makedirs("events")
else :
    print("Directory already exists, removing all files and recreating the directory...")
    shutil.rmtree("events")
    os.makedirs("events")
    

def save_to_json(event):
    file_name=f"events/{event['title']}"
    with open(f'{file_name}.json', 'w', encoding='utf-8') as json_file:
        json.dump(event, json_file, ensure_ascii=False, indent=4)

for event in events_results:
    save_to_json(event)
