import flask
from flask import Flask, jsonify, request, render_template
from flask_restful import reqparse, abort, Api, Resource
from lib_sqlconnect import *

ex = SQLConnect()
app = Flask(__name__)
api = Api(app)


@app.route('/admin/teachers-list')
def teachers_list_view():
    teachers = ex.get(User)

    return flask.render_template('teachers_list.html', teachers=teachers)


@app.route('/admin/teachers-list/edit')
def teachers_list_view_edit():
    id = request.args.get('id')
    first_name = request.args.get('first_name')
    middle_name = request.args.get('middle_name')
    last_name = request.args.get('last_name')
    status = request.args.get('status')
    position = request.args.get('position')
    password = request.args.get('password')

    # print(id, first_name, )

    user = ex.get(User, "id", id, True)

    if user:
        print("\n\n******\n\n")
        if first_name:
            user.first_name = first_name
        if middle_name: user.middle_name = middle_name
        if last_name: user.last_name = last_name
        if status: user.status = status
        if position: user.position = position
        if password: user.password = password


    else:
        user = User(
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    status=status,
                    position=position,
                    password=password,
                    )
        ex.add(user)

    ex.commit()



    print('!!!!!!!!!!', user)

    if ex.get(User, "id", id):
        ...

    print(id, first_name)

    return ''


# api.add_resource(teachers_list_view, '/teacher-list')

if __name__ == '__main__':
    app.run(debug=True)
