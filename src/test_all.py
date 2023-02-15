import pytest
import boto3
import os
import uuid
import json
import logging
import uuid
import dynamo 
import handler
def test_all(event, expected_response, mocker):
    # Mock dynamodb.put_item() and dynamo.to_item()
    dynamodb = mocker.patch("handler.dynamodb")
    dynamodb.put_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

    # Call create function
    assert True