from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from lib_sqlconnect.models import Course, CourseTask
from lib_sqlconnect.sqlconnect import SQLConnect


class CourseTaskResource(Resource):  # Надо переименовать класс Моделей, чтобы тут не было два раза Ресурсы
    __tablename__ = 'course_task'

    sql_conn = SQLConnect()
    parser = reqparse.RequestParser()

    arg_dict = {'name': 'the task cannot be without a name',
                'course_id': 'the task cannot be without a course_id',
                'task': 'the task cannot be without a description',
                'res': 'the task cannot be without a result'
                }

    for i in arg_dict:
        parser.add_argument(i,
                            type=str,
                            required=True,
                            help=arg_dict[i])

    # @jwt_required()
    def get(self, _id):
        course_task = self.sql_conn.get(CourseTask, 'id', _id, True)

        if course_task:
            return {'message': course_task.json()}
        return {'message': 'not found'}, 404

    def put(self, _id):
        data = self.parser.parse_args()

        course_task = self.sql_conn.get(CourseTask, 'id', _id, True)

        if course_task is None:
            course_task = CourseTask(**data)
            self.sql_conn.add(course_task)
        else:
            course_task.name = data['name']
            course_task.course_id = data['course_id']
            course_task.task = data['task']
            course_task.res = data['res']

        self.sql_conn.commit()

        return {'course task': course_task.json()}

    def delete(self, _id):
        course_task = self.sql_conn.get(CourseTask, 'id', _id, True)

        if course_task:
            self.sql_conn.delete(course_task)
            self.sql_conn.commit()

        return {'message': 'Item has deleted'}


class CourseTaskList(Resource):
    sql_conn = SQLConnect()

    parser = reqparse.RequestParser()

    arg_dict = {'name': 'a task cannot be without a name',
                'task': 'a task cannot be without a description',
                'res': 'a task cannot be without a result'
                }

    for i in arg_dict:
        parser.add_argument(i,
                            type=str,
                            required=True,
                            help=arg_dict[i])

    def get(self, slug_name):

        course = self.sql_conn.get(Course, 'slug_name', slug_name, True)

        if course is None:
            return {'message': 'course with this slug_name does not exist'}

        return {'course tasks': [task.json() for task in course.course_task]}

    def post(self, slug_name):

        course = self.sql_conn.get(Course, "slug_name", slug_name, True)

        if course is None:
            return {'message': 'course with this slug_name does not exist'}

        data = self.parser.parse_args()

        course_task = CourseTask(course_id=course.id, **data)

        self.sql_conn.add(course_task)
        self.sql_conn.commit()

        return {"course_task": course_task.json()}, 201
