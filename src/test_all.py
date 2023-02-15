import pytest
import boto3
import os
import uuid
import json
import logging
import uuid
import dynamo 
import handler
@pytest.mark.parametrize("event, expected_response", [
    ({"body": '{"name": "Alex", "last_name": "Illescas"}'},
     {"statusCode": 200, "body": "Successfully created."}),
    ({"body": '{"name": "Alexander", "last_name": "Illescas"}'},
     {"statusCode": 500, "body": "An error occured while creating post."})
])
def test_all(event, expected_response, mocker):
    # Mock dynamodb.put_item() and dynamo.to_item()
    dynamodb = mocker.patch("handler.dynamodb")
    dynamodb.put_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

    # Call create function
    assert True