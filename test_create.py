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


def test_create():
    os.environ['DYNAMODB_TABLE'] = 'test-table'
    os.environ['DESTINATION_TABLE'] = 'test-table-destination'
    event = {
        'body': json.dumps({
            'name': 'Juan',
            'last_name': 'Perez'
        })
    }
    context = {}
    # Mock the DynamoDB client and its put_item method
    mock_client = MagicMock()
    mock_client.put_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
    with patch('boto3.client', return_value=mock_client):
        # Call the function and get the response
        response = handler.create(event, context)

    # Check the response
    assert response['statusCode'] == 200
    assert response['body'] == 'Successfully created.'
    # Check that the item was actually created in DynamoDB
    mock_client.put_item.assert_called_once()
    args, kwargs = mock_client.put_item.call_args
    assert kwargs['TableName'] == 'test-table'
    assert kwargs['Item']['name']['S'] == 'Juan'
    assert kwargs['Item']['last_name']['S'] == 'Perez'