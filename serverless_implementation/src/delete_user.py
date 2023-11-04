import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserTable')

def delete(event, context):
    id = event['pathParameters']['id']

    try:
        table.delete_item(Key={'id': id})
        response = {
            'statusCode': 200,
            'body': json.dumps({'message': 'User deleted successfully'})
        }
    except ClientError as e:
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    return response