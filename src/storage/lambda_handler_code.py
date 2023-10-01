import json
import boto3
import urllib.parse

print("loading function")

s3 = boto3.client('s3')
def lambda_handler(event, context):
    # TODO implement
    
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        # Get the object from S3
        response = s3.get_object(
            Bucket=bucket_name,
            Key=object_key
        )
        
        # Read the content of the object
        content = response['Body'].read().decode('utf-8')
        
        # Process the content (in this example, we're just printing it)
        print(f'Content of {object_key}:')
        print(content)
        
        return {
            'statusCode': 200,
            'body': 'Object content retrieved successfully'
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': f'Error accessing object: {e}'
        }
