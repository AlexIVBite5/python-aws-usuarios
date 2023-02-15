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


def test_all():
    os.environ['DYNAMODB_TABLE'] = 'test-table'
    event = {
        'body': json.dumps({
            'name': 'John',
            'last_name': 'Doe'
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
    assert kwargs['TableName'] == 'test_table'
    assert kwargs['Item']['name']['S'] == 'John'
    assert kwargs['Item']['last_name']['S'] == 'Doe'
    assert 'createdAt' in kwargs['Item']
    assert 'id' in kwargs['Item']