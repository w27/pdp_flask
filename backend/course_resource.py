from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from lib_sqlconnect.models import Course, CourseTask
from lib_sqlconnect.sqlconnect import SQLConnect


class CourseResource(Resource):  # Надо переименовать класс Моделей, чтобы тут не было два раза Ресурсы
    __tablename__ = 'courses'

    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='the course cannot be without a name')

    parser.add_argument('key',
                        type=str,
                        required=True,
                        help='the course cannot be without a key')

    parser.add_argument('slug_name',
                        type=str,
                        required=True,
                        help='the course cannot be without a slug name')

    sql_conn = SQLConnect()

    @jwt_required()
    def get(self, slug_name):  # надо поменять title и name местами, потому что title всё-таки нечто большее чем

        course = self.sql_conn.get(Course, 'slug_name', slug_name, True)

        if course:
            return {'message': course.json()}

        return {'message': 'not found'}, 404

    @jwt_required()
    def put(self, slug_name):
        data = self.parser.parse_args()

        course = self.sql_conn.get(Course, 'slug_name', slug_name, True)

        if course is None:
            course = Course(slug_name=slug_name, **data)
            self.sql_conn.add(course)
        else:
            course.name = data['name']
            course.key = data['key']

        self.sql_conn.commit()

        return {'message': course.json()}

    @jwt_required()
    def delete(self, slug_name):
        course = self.sql_conn.get(Course, 'slug_name', slug_name, True)

        if course:

            self.sql_conn.delete(course)
            self.sql_conn.commit()

        return {'message': 'Course has deleted'}


class CourseList(Resource):
    sql_conn = SQLConnect()

    @jwt_required()
    def get(self):

        return {'course list': [course.json() for course in self.sql_conn.get(Course)]}

    @jwt_required()
    def post(self):

        data = CourseResource.parser.parse_args()

        if self.sql_conn.get(Course, 'slug_name', data['slug_name']):
            return {'message': 'A course with this name already exists'}, 400

        course = Course(**data)

        self.sql_conn.add(course)
        self.sql_conn.commit()

        return {'message': course.json()}, 201
