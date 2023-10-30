import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def create_user(event, context):
    body = json.loads(event['body'])
    id = body['id']
    name = body['name']
    email = body['email']
    tags = body['tags']

    response = table.put_item(
        Item={
            'id': id,
            'name': name,
            'email': email,
            'tags': tags
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'User created successfully'})
    }



def get_user(event, context):
    id = event['pathParameters']['id']

    response = table.get_item(
        Key={'id': id}
    )

    if 'Item' in response:
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'User not found'})
        }
        
def update_user(event, context):
    id = event['pathParameters']['id']
    body = json.loads(event['body'])
    name = body['name']
    email = body['email']
    tags = body['tags']

    response = table.update_item(
        Key={'id': id},
        UpdateExpression='SET name = :name, email = :email, tags = :tags',
        ExpressionAttributeValues={':name': name, ':email': email, ':tags': tags},
        ReturnValues='ALL_NEW'
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response['Attributes'])
    }
    
def delete_user(event, context):
    id = event['pathParameters']['id']

    response = table.delete_item(
        Key={'id': id}
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'User deleted successfully'})
    }