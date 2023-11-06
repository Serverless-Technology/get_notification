import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Users")


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event,
    }
    print(event)
    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """


def create_user(event, context):
    body = json.loads(event["body"])
    id = body["id"]
    name = body["name"]
    email = body["email"]
    tags = body["tags"]

    response = table.put_item(
        Item={"id": id, "name": name, "email": email, "tags": tags}
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "User created successfully"}),
    }
