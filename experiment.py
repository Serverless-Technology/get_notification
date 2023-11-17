import os
import json
from dotenv import load_dotenv

def get_data(file_path):
    tag_message = ""
    f = open(file_path)
    data = dict(json.load(f))
    title = data['title']
    date = data['date']['when']
    address = data['address'][0]
    link=data['link']
    tag_message=f"<b>Title: {title}</b> <br> Date: {date} <br> Address: {address} <br> Link: {link} <br>"
    
    return tag_message

def parse_json(dir):
    file_list = os.listdir(dir)
    message=""
    for tag_dir in file_list:
        tag_dir = f"{dir}/{tag_dir}"
        tags = os.listdir(tag_dir)
        for tag in tags:
            tag = f"{tag_dir}/{tag}"
            tag_message = get_data(tag)
            message+=f"<br> {tag_message}"

    return message


load_dotenv()


FILEDIR = os.environ.get("SRC_PATH")

parse_json(FILEDIR)
