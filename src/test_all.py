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
                "name": {"S": "John"},
                "surname": {"S": "Doe"}
            },
            {
                "id": {"S": "5678"},
                "name": {"S": "Jane"},
                "surname": {"S": "Smith"}
            }
        ]
    }
    with patch('boto3.client', return_value=mock_dynamodb_client):
        # Ejecuta la función all
        result = handler.all({}, {})
        # Verifica que la respuesta sea la esperada
        assert result['statusCode'] == 200
        assert result['body'] == '[{"id": "1234", "name": "John", "surname": "Doe"}, {"id": "5678", "name": "Jane", "surname": "Smith"}]'
        assert {"id": "1234", "name": "John", "surname": "Doe"} in result['body']
        assert {"id": "5678", "name": "Jane", "surname": "Smith"} in result['body']

