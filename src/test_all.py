import pytest
import boto3
import os
import uuid
import json
import logging
import uuid
import dynamo 
import handler
from unittest.mock import MagicMock, patch, Mock


def test_all():
    os.environ['DYNAMODB_TABLE'] = 'test-table'
    mock_dynamodb_client = MagicMock()
    mock_dynamodb_client.scan.return_value = {
        "Items": [
            {
                "id": {"S": "1234"},
                "name": {"S": "Juan"},
                "last_name": {"S": "Lopez"}
            }
        ]
    }
    mock_to_dict = MagicMock(return_value={"id": "1234", "name": "Juan", "last_name": "Lopez"})
    

    with patch('boto3.client', return_value=mock_dynamodb_client), patch('handler.dynamo.to_dict', new=mock_to_dict):
        # Ejecuta la función all
        result = handler.all({}, {})
        # Verifica que la respuesta sea la esperada
        assert result['statusCode'] == 200
        assert result['body'] == '[{"id": "1234", "name": "Juan", "last_name": "Lopez"}]'

    expected_response = {
        "statusCode": 200,
        "body": json.dumps([{"id": "1234", "name": "Juan", "last_name": "Lopez"}])
    }
    assert result == expected_response
       
