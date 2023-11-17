import os
import requests
import json
from flask import current_app

from dotenv import load_dotenv

load_dotenv()

SENDER_MAIL = os.environ.get("SENDER_MAIL")
# RECEIVER_MAIL = current_app.config["session"].get("email")
MAIL_SUBJECT = "Event Notification"
FILEDIR = os.environ.get("SRC_PATH")

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


def send_mail(
    sender: str,
    subject: str,
    receivers: list = None,
    attachments: list = None,
):
    key = os.environ.get("MAILGUN_API_KEY")
    # attachments = [
    # ("attachment", ("data1.json", open("events/3.json", "rb").read())),
    # ("attachment", ("data2.json", open("events/4.json", "rb").read())),
    # ]
    # message = "Json data: \n"
    # with open("events/3.json", "r") as file:
    #     json_content = json.load(file)
    #     message += json.dumps(json_content, indent=4)
    # print(message)
    print(key)
    assert key != None, f"Mailgun API key is required: {key}"
    assert sender != None, "Sender email address is required"
    assert receivers != None, "Receiver email address is required"
    
    # Parse JSON
    message = parse_json(FILEDIR)
    response = requests.post(
        "https://api.mailgun.net/v3/sandboxab704171788e415e86350efc6b4b9160.mailgun.org/messages",
        auth=("api", key),
        files=attachments,
        data={"from": sender, "to": receivers, "subject": subject, "html": message},
    )

    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print(f"Error sending email: {response.status_code} - {response.text}")

    return response


def notify(event, context):
    # receiver = list(RECEIVER_MAIL)
    sender = SENDER_MAIL
    subject = MAIL_SUBJECT
    print(event)
    bucket_name = event["Records"]["s3"]["bucket"]["name"]
    file_name = event["Records"]["s3"]["object"]["key"]
    response = {
        "body": event,
        "status": 200
    }
    return response
    # response = send_mail(sender, subject, event, receiver)
    # if response.status_code == 200:
    #     print("Email sent successfully!")
    # else:
    #     print(f"Error sending email: {response.status_code} - {response.text}")
    # return response
