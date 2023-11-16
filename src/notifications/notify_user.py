import os
import requests
import json
from flask import current_app

SENDER_MAIL = os.environ.get('SENDER_MAIL')
SENDER_NAME = os.environ.get('SENDER_NAME')
RECEIVER_MAIL = current_app.config['session'].get('email')
MAIL_SUBJECT = "Event Notification"

def send_mail(sender: str, subject: str, body: str, receivers: list = None, attachments: list = None):
    key = os.environ.get('MAILGUN_API_KEY')
    # attachments = [
    # ("attachment", ("data1.json", open("events/3.json", "rb").read())),
    # ("attachment", ("data2.json", open("events/4.json", "rb").read())),
    # ]
    # message = "Json data: \n"
    # with open("events/3.json", "r") as file:
    #     json_content = json.load(file)
    #     message += json.dumps(json_content, indent=4)
    # print(message)
    response =  requests.post(
		"https://api.mailgun.net/v3/sandboxab704171788e415e86350efc6b4b9160.mailgun.org/messages",
		auth=("api", key),
        files=attachments,
		data={"from": sender,    
			"to": receivers,
			"subject": subject,
			"text": body})
    return response
    # if response.status_code == 200:
    #     print('Email sent successfully!')
    # else:
    #     print(f'Error sending email: {response.status_code} - {response.text}')

def notify(event,context):
    receiver = list(RECEIVER_MAIL)
    sender = SENDER_NAME + "<" + SENDER_MAIL + ">"
    subject = MAIL_SUBJECT
    response = send_mail(sender, subject,event, receiver)
    if response.status_code == 200:
        print('Email sent successfully!')
    else:
        print(f'Error sending email: {response.status_code} - {response.text}')
    return response