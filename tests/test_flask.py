import pytest
import json
from app import app
from lib_sqlconnect.sqlconnect import SQLConnect, start_build

# start_build()


def test_base_route():
    client = app.test_client()
    response = client.get('/')
    assert b"Hello World!" in response.get_data()
    assert response.status_code == 200



def test_base_courses():
    client = app.test_client()
    response = client.post("/auth", data=json.dumps({
        "username": "dima",
        "password": "1234"
    }),headers={"Content-Type": "application/json"})
    access_token = response.get_json().get("access_token")
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    response = app.test_client().get("/courses", headers=headers)
    assert "course list" in response.get_json()
    assert response.status_code == 200

test_base_courses()