from src.handler import all
import pytest

def test_create():
    response = all()
    print(response)
    assert response.statusCode == 200
    #assert response.content is not None
    #lista = response.json()["body"]
    #assert isinstance(lista, list)