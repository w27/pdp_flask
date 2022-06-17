import flask
# from files.sql_conn import *
from lib_sqlconnect import *
from sqlalchemy import Boolean

app = flask.Flask(__name__)

base = Base
my_engine = create_engine(f'postgresql+psycopg2://assistent:0123456!6543210@94.19.251.222:25008/ass_db',
                                    echo=False)
my_session = sessionmaker(bind=my_engine)()




@app.route("/")
def test_get():
    all_users = my_session.query(Student).all()


    users_list = []
    for user in all_users:
        buf = []
        buf.append(user.id)
        buf.append(user.first_name)
        buf.append(user.last_name)

        user_courses = my_session.query(StudentCourse).filter(StudentCourse.student_id == user.id).all()

        buf_2 = []
        for course in user_courses:
            course_name = my_session.query(Course).filter(Course.id == course.course_id).first().name

            buf_2.append(course_name)

        buf.append(buf_2)

        users_list.append(buf)

    return flask.render_template('index.html', users_list=users_list)



class Category(Base):
    __tablename__ = "user_category"
    category = Column(String, primary_key=True)


category_1 = Category(category='Админ')
category_2 = Category(category='Преподаватель')
category_3 = Category(category='Студент')

my_session.add(category_1)
my_session.add(category_2)
my_session.add(category_3)




class NewUser(Base):  # заменить класс User на этот класс, но позже
    __tablename__ = "new_user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    category = Column(String, ForeignKey("user_category.category"))
    active = Column(Boolean, default=True)




# @app.route("/test_get/<string:h>")
# def test_post(h):
#     print(h)
#     return flask.render_template('index.html')



if __name__ == "__main__":

    app.run(debug=True)


