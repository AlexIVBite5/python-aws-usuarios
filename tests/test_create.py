import boto3
import json
import os
import pytest
import uuid
from datetime import datetime
from moto import mock_dynamodb2

from src.handler import create

@mock_dynamodb2
def test_create_user():
    os.environ['DYNAMODB_TABLE'] = 'test-table'
    dynamodb = boto3.client('dynamodb')
    dynamodb.create_table(
        TableName=os.environ['DYNAMODB_TABLE'],
        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}]
    )

    event = {
        'body': json.dumps({
            'name': 'juan',
            'last_name': 'lopez'
        })
    }

    response = create(event, {})
    assert response['statusCode'] == 200
    assert response['body'] == 'Successfully created.'