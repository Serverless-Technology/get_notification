# import base64
# from email.message import EmailMessage

# import google.auth
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError


# def gmail_send_message():
#     """Create and send an email message
#     Print the returned  message id
#     Returns: Message object, including message id

#     Load pre-authorized user credentials from the environment.
#     TODO(developer) - See https://developers.google.com/identity
#     for guides on implementing OAuth2 for the application.
#     """
#     creds, _ = google.auth.default()

#     try:
#         service = build('gmail', 'v1', credentials=creds)
#         message = EmailMessage()

#         message.set_content('This is automated draft mail hahaha!')

#         message['To'] = 'mann.jain@iitgn.ac.in'
#         message['From'] = 'mannjain777@gmail.com'
#         message['Subject'] = 'Automated draft'

#         # encoded message
#         encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
#             .decode()

#         create_message = {
#             'raw': encoded_message
#         }
#         # pylint: disable=E1101
#         send_message = (service.users().messages().send
#                         (userId="me", body=create_message).execute())
#         print(F'Message Id: {send_message["id"]}')
#     except HttpError as error:
#         print(F'An error occurred: {error}')
#         send_message = None
#     return send_message


# if __name__ == '__main__':
#     gmail_send_message()

import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

def send_simple_message():
    key = os.environ.get('MAILGUN_API_KEY')
    attachments = [
    ("attachment", ("data1.json", open("events/3.json", "rb").read())),
    ("attachment", ("data2.json", open("events/4.json", "rb").read())),
    ]
    # message = "Json data: \n"
    # with open("events/3.json", "r") as file:
    #     json_content = json.load(file)
    #     message += json.dumps(json_content, indent=4)
    # print(message)
    response =  requests.post(
		"https://api.mailgun.net/v3/sandboxab704171788e415e86350efc6b4b9160.mailgun.org/messages",
		auth=("api", key),
        files=attachments,
		data={"from": "Mann Jain <mann.jain@iitgn.ac.in>",    
			"to": ["mannjain777@gmail.com"],
			"subject": "Hello, Trial Email",
			"text": "Testing some Mailgun awesomeness!"})
    if response.status_code == 200:
        print('Email sent successfully!')
    else:
        print(f'Error sending email: {response.status_code} - {response.text}')

if __name__ == '__main__':
    send_simple_message()