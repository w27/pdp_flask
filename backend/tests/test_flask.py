import pytest
import json
import os
from app import app
from lib_sqlconnect.sqlconnect import SQLConnect, start_build
from lib_sqlconnect.models import Course, CourseTask



path = "test.sqlite"
if os.path.exists(path):
    os.system("rm " + path)


sql = SQLConnect()

start_build()

client = app.test_client()
response = client.post("/auth", data=json.dumps({
    "username": "dima",
    "password": "1234"
}),headers={"Content-Type": "application/json"})

access_token = response.get_json().get("access_token")
headers = {
    "Content-Type": "application/json",
    'Authorization': 'Bearer {}'.format(access_token)
}

def test_base_route():
    response = client.get('/')
    assert b"DOCTYPE html" in response.get_data()
    assert response.status_code == 200

def test_base_courses_get():
    response = client.get("/courses", headers=headers)
    assert "course list" in response.get_json()
    assert response.status_code == 200

def test_base_courses_post():

    buf = sql.get(Course, 'slug_name', "py-100", one=True)
    if buf:
        sql.delete(buf)
        sql.commit()

    response = client.post("/courses", data=json.dumps({
        "name": "tt01",
        "key": "tt01",
        "slug_name": "py-100"
    }),headers=headers)
    assert {'message': {'id': 4, 'key': 'tt01', 'name': 'tt01', 'slug_name': 'py-100'}} == response.get_json()
    assert response.status_code == 201

def test_base_course_put():
    response = client.put("/course/py-100", data=json.dumps({
        "name": "tt01",
        "key": "tt01",
        "slug_name": "py-100"
    }), headers=headers)
    assert {'message': {'id': 4, 'key': 'tt01', 'name': 'tt01', 'slug_name': 'py-100'}} == response.get_json()
    assert response.status_code == 200

def test_base_course_get():
    response = client.get("/course/py-100", headers=headers)
    assert {'message': {'id': 4, 'key': 'tt01', 'name': 'tt01', 'slug_name': 'py-100'}} == response.get_json()
    assert response.status_code == 200

def test_base_course_delete():
    response = client.delete("/course/py-100", data=json.dumps({
        "name": "tt01",
        "key": "tt01",
        "slug_name": "py-100"
    }), headers=headers)
    assert {'message': 'Course has deleted'} == response.get_json()
    assert response.status_code == 200