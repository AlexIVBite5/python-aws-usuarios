from datetime import datetime
import boto3
import os
import uuid
import json
import logging
import uuid
import dynamo  # helper function


#logger = logging.getLogger()
#logger.setLevel(logging.INFO)
dynamodb = boto3.resource('dynamodb', region_name=str(os.environ['REGION_NAME']))
table_name = str(os.environ['DYNAMODB_TABLE'])
destination_table_name = str(os.environ['DESTINATION_TABLE'])

def create(event, context):
    #logger.info(f'Incoming request is: {event}')

    # Set the default error response
    response = {
        "statusCode": 500,
        "body": "An error occured while creating post."
    }

    post_str = event['body']
    post = json.loads(post_str)
    post['createdAt'] = datetime.now().isoformat()
    post['id'] = str(uuid.uuid4())

    res = dynamodb.put_item(
        TableName=table_name,
        Item={
            'id': {'S': post['id']},
            'name': {'S': post['name']},
            'last_name': {'S': post['last_name']},
            'created_at': {'S': post['createdAt']}
        }
    )

    # If creation is successful
    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        response = {
            "statusCode": 200,
            "body": "Successfully created."
        }

    return response


def get(event, context):
    #logger.info(f'Incoming request is: {event}')
    # Set the default error response
    response = {
        "statusCode": 500,
        "body": "An error occured while getting post."
    }

    post_id = event['pathParameters']['userId']

    post_query = dynamodb.get_item(
        TableName=table_name, Key={'id': {'S': post_id}})

    if post_query['ResponseMetadata']['HTTPStatusCode'] == 200:
        if 'Item' in post_query:
            post = post_query['Item']
            #logger.info(f'Post is: {post}')
            response = {
                "statusCode": 200,
                'headers': {'Content-Type': 'application/json'},
                "body": json.dumps(dynamo.to_dict(post))
            }

    return response


def all(event, context):
    # Set the default error response
    scan_result = dynamodb.scan(TableName=table_name)['Items']
    posts = []
    #print(scan_result)
    for item in scan_result:
        posts.append(dynamo.to_dict(item))
    response = {
        "statusCode": 200,
        "body": json.dumps(posts)
    }
    return response

def replication(event, context):
    # Set the default error response
    print(destination_table_name)
    response = {
        "statusCode": 500,
        "body": "An error occurred while replicating the post"
    }

    for record in event["Records"]:
        if record["eventName"] == "INSERT":
            new_item = record["dynamodb"]["NewImage"]
            print(new_item)
            item = {
                'id': new_item['id']['S'],
                'name': new_item['name']['S'],
                'last_name': new_item['last_name']['S'],
            }
            res = dynamodb.put_item(
                TableName=destination_table_name,
                Item=dynamo.to_item(item)
            )
            if res['ResponseMetadata']['HTTPStatusCode'] == 200:
                response = {
                    "statusCode": 200,
                    "body": "Successful replication."
                }
      
    return response

