from flask_jwt_extended import JWTManager

from flask import Flask, render_template, send_from_directory
from flask_restful import Api
# from flask_jwt import JWT

from course_resource import CourseList, CourseResource
from task_resource import CourseTaskResource, CourseTaskList
from user_resource import UserResource, UserLogin
from flask_cors import CORS, cross_origin
from flask_restful import Resource, reqparse

import os


app = Flask(__name__)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
# app.config['CORS_HEADERS'] = 'Content-Type'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'dimka'
api = Api(app)

# jwt = JWT(app, authenticate, identity)  # создаёт endpoint - /auth

jwt = JWTManager(app)

api.add_resource(CourseResource, '/course/<string:slug_name>')      # поменять класс - убрать Resourse
api.add_resource(CourseList, '/courses')

api.add_resource(CourseTaskResource, '/task/<int:_id>')             # поменять класс - убрать Resourse
api.add_resource(CourseTaskList, '/tasks/<string:slug_name>')

api.add_resource(UserResource, '/user/<int:_id>')                   # поменять класс - убрать Resourse
# api.add_resource(UserList, '/users')
api.add_resource(UserLogin, '/auth')                                # но непонятно, будет ли так работать.


class CorsOptions(Resource):
    def options(self):
        return {'task': 'Hello world'}, 201, {'Access-Control-Allow-Origin': '*'}

api.add_resource(CorsOptions, '/courses')

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.route("/")
def home():  
    return render_template('index.html')


CORS(app, origins="http://localhost:3000", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True)

def main():
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()
