import hmac

from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    # jwt_refresh_token_required,      #TokenRefresh
    get_jwt_identity,
    # get_raw_jwt,                     # UserLogout
    jwt_required
)

from lib_sqlconnect.models import User
from lib_sqlconnect.sqlconnect import SQLConnect

from flask import render_template

arg_dict = {'first_name': 'a user cannot be without a first_name',
            'middle_name': 'a user cannot be without a middle_name',
            'last_name': 'a user cannot be without a last_name',
            'status': 'a user cannot be without a status',
            'position': 'a user cannot be without a position',
            'username': 'a user cannot be without a username',
            'password': 'a user cannot be without a password'
            }


class UserResource(Resource):
    sql_conn = SQLConnect()
    parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, _id):

        user_id = get_jwt_identity()
        print([user.__repr__() for user in self.sql_conn.get(User)], user_id)
        user = self.sql_conn.get(User, 'id', _id, True)

        if user is None:
            return {'message': 'not found'}, 404

        return {'user': user.json()}

    def put(self, _id):
        data = self.parser.parse_args()

        user = self.sql_conn.get(User, 'id', _id, True)

        if user is None:
            user = User(**data)
            self.sql_conn.add(user)
        else:
            user.first_name = data['first_name']
            user.middle_name = data['middle_name']
            user.last_name = data['last_name']
            user.status = data['status']
            user.position = data['position']
            user.username = data['username']
            user.password = data['password']

        self.sql_conn.commit()

        return {'course task': user.json()}

    def delete(self, _id):
        user = self.sql_conn.get(User, 'id', _id, True)

        if user:
            self.sql_conn.delete(user)
            self.sql_conn.commit()

        return {'message': 'User has deleted'}


# class UserList(Resource):
#     sql_conn = SQLConnect()
#     parser = reqparse.RequestParser()
#
#     def get(self):
#         users = self.sql_conn.get(User)
#
#         return {'users': [user.json() for user in users]}




class UserLogin(Resource):
    sql_conn = SQLConnect()
    parser = reqparse.RequestParser()

    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='A user cannot be without a username')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='A user cannot be without a password')

    def post(self):
        data = self.parser.parse_args()

        user = self.sql_conn.get(User, 'username', data['username'], True)

        if user and hmac.compare_digest(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200

        return {'message': 'Invalid password'}, 401


"""
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    status = Column(Boolean, default=True)
    position = Column(Integer, nullable=False)
    password = Column(String)
"""