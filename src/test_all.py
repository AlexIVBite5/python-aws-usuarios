import pytest
import boto3
import os
import uuid
import json
import logging
import uuid
import dynamo 
import handler
import moto 

@moto.mock_dynamodb2
def test_all():
    os.environ['DYNAMODB_TABLE'] = 'test-table'
    dynamodb = boto3.client('dynamodb')
    dynamodb.create_table(
        TableName=os.environ['DYNAMODB_TABLE'],
        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}]
    )

    event = {
        'body': json.dumps({
            'name': 'John',
            'last_name': 'Doe'
        })
    }

    response = handler.create(event, {})
    assert response['statusCode'] == 200
    assert response['body'] == 'Successfully created.'