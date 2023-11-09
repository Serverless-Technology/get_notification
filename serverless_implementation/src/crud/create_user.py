import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserTable')

def create(event, context):
    data = json.loads(event['body'])
    id = data['id']
    name = data['name']
    email = data['email']
    tags = data['tags']

    try:
        table.put_item(
            Item={
                'id': id,
                'name': name,
                'email': email,
                'tags': tags
            }
        )
        response = {
            'statusCode': 200,
            'body': json.dumps({'message': 'User created successfully'})
        }
    except ClientError as e:
        response = {
            'statusCode': 500,
            'body': json.dumps({
                'fields':f"{id}, {name}, {email}, {tags}",
                'error': str(e)
                })
        }

    return response