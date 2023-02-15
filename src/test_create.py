import json
from datetime import datetime
from uuid import UUID, uuid4
import pytest
import handler

def test_create(event, expected_response, mocker):
    

    # Check response
    assert True