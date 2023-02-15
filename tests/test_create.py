import pytest
from src.handler import create
import json
from datetime import datetime
from uuid import UUID, uuid4



@pytest.mark.parametrize("event, expected_response", [
    ({"body": '{"name": "Alex", "last_name": "Illescas"}'},
     {"statusCode": 200, "body": "Successfully created."}),
    ({"body": '{"name": "Alex", "last_name": "Illescas"}'},
     {"statusCode": 500, "body": "An error occured while creating post."})
])
def test_create(event, expected_response, mocker):
    # Mock dynamodb.put_item() and dynamo.to_item()
    dynamodb = mocker.patch("lambda_function.dynamodb")
    dynamo = mocker.patch("lambda_function.dynamo")
    dynamo.to_item.return_value = {"id": str(uuid4()), "name": "Alex", "last_name": "Illescas", "createdAt": datetime.now().isoformat()}
    dynamodb.put_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

    # Call create function
    response = create(event, None)

    # Check response
    assert response == expected_response