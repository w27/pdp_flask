from flask_jwt_extended import JWTManager

from flask import Flask, render_template, send_from_directory
from flask_restful import Api
# from flask_jwt import JWT

from course_resource import CourseList, CourseResource
from task_resource import CourseTaskResource, CourseTaskList
from user_resource import UserResource, UserLogin

import os


app = Flask(__name__)
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

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.route("/")
def home():  
    return render_template('index.html')



def main():
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()
