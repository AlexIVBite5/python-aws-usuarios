import pytest
import boto3
import os
import uuid
import json
import logging
import uuid
import dynamo 
import handler
from unittest.mock import MagicMock, patch


def test_replication():
    os.environ['DESTINATION_TABLE'] = 'test-table-destination'
    event = {
        "Records": [
            {
                "eventName": "INSERT",
                "dynamodb": {
                    "NewImage": {
                        "id": {"S": "1"},
                        "name": {"S": "Juan"},
                        "last_name": {"S": "Perez"},
                        "created_at": {"S": "2022-01-01 00:00:00"}
                    }
                }
            }
        ]
    }
    context = {}
    # Mock the DynamoDB client and its put_item method
    mock_client = MagicMock()
    mock_client.put_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
    with patch('boto3.client', return_value=mock_client):
        # Call the function and get the response
        response = handler.replication(event, context)

    # Check the response
    assert response['statusCode'] == 200
    assert response['body'] == 'Successfully created.'