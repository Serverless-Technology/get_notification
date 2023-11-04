import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserTable')

def get_users(event, context):
    try:
        response = table.scan()
        print(response)
        users = response['Items']
        response = {
            'statusCode': 200,
            'body': json.dumps(users)
        }
    except ClientError as e:
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    return response