# import flask
# from flask_restful import Resource, Api
#
# from lib_sqlconnect import *
#
# app = flask.Flask(__name__)
#
# connect = SQLConnect()
#
#
# @app.route('/')
# def view_index():
#
#     return flask.render_template('index.html')
#
#
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource

import flask
from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        un = json_data['username']
        pw = json_data['password']
        print(un, pw)
        return jsonify(u=un, p=pw)


api.add_resource(HelloWorld, '/testing')


@app.route('/')
def view_index():
    return flask.render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
