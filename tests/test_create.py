from src.handler import create
import pytest

def test_create():
    data={
        "name":"Israel",
        "last_name":"Lopez"
    }
    respuesta_positiva = {
        "statusCode": 200,
        "body": "Successfully created."
    }
    assert create(event=data)==respuesta_positiva