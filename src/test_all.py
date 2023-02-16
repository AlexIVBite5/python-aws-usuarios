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
    dynamodb_mock = Mock()
    dynamodb_mock.scan.return_value = {
        "Items": [
            {
                "id": {"S": "1"},
                "title": {"S": "Test post 1"},
                "content": {"S": "This is the first test post."},
                "createdAt": {"S": "2022-01-01T00:00:00.000000"},
                "updatedAt": {"S": "2022-01-01T00:00:00.000000"}
            },
            {
                "id": {"S": "2"},
                "title": {"S": "Test post 2"},
                "content": {"S": "This is the second test post."},
                "createdAt": {"S": "2022-01-02T00:00:00.000000"},
                "updatedAt": {"S": "2022-01-02T00:00:00.000000"}
            }
        ]
    }

    # Call the function with the mock event and context
    response = handler.all({}, {}, dynamodb=dynamodb_mock)

    # Check that the response is correct
    expected_response = {
        "statusCode": 200,
        "body": json.dumps([
            {
                "id": "1",
                "title": "Test post 1",
                "content": "This is the first test post.",
                "createdAt": "2022-01-01T00:00:00.000000",
                "updatedAt": "2022-01-01T00:00:00.000000"
            },
            {
                "id": "2",
                "title": "Test post 2",
                "content": "This is the second test post.",
                "createdAt": "2022-01-02T00:00:00.000000",
                "updatedAt": "2022-01-02T00:00:00.000000"
            }
        ])
    }
    assert response == expected_response