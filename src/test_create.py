import json
from datetime import datetime
from uuid import UUID, uuid4
import pytest
import handler

def test_create(event, expected_response, mocker):
    # Mock dynamodb.put_item() and dynamo.to_item()
    dynamodb = mocker.patch("handler.dynamodb")
    dynamodb.put_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

    # Call create function
    response = handler.create(event, None)

    # Check response
    assert response == expected_response