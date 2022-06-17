from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
import json

Base = declarative_base()


class CourseList(Base):
    __tablename__ = "course_list"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    key = Column(String)

    def __repr__(self):
        return f"<CourseList(id={self.id}, name='{self.name}', key='{self.key}')>"


class SQLConnect:
    def __init__(self, base, name_user: str, pass_user: str, host_bd: str, port, name_db: str, echo=False):
        self.base = base
        self.engine = create_engine(f'postgresql+psycopg2://{name_user}:{pass_user}@{host_bd}:{port}/{name_db}',
                                    echo=echo)
        self.session = sessionmaker(bind=self.engine)()
        self.base.metadata.create_all(self.engine)

    def clean_db(self):
        self.session.close()
        self.base.metadata.drop_all(self.engine)

    def add(self, obj):
        self.session.add(obj)

    def commit(self):
        self.session.commit()


class SQLAss:
    def __init__(self, path, base):
        with open(path) as file:
            conf_sql = json.load(file)

        self.name_user = conf_sql["name_user"]
        self.pass_user = conf_sql["pass_user"]
        self.host_bd = conf_sql["host_bd"]
        self.port = conf_sql["port"]
        self.name_db = conf_sql["name_db"]
        self.echo = conf_sql["echo"]

        self.conn = SQLConnect(base, self.name_user, self.pass_user, self.host_bd, self.port, self.name_db, self.echo)

    def start_build(self):
        self.conn.clean_db()
        # Или пересоздать self.conn (чтоб сработал еще раз инит)
        self.conn.session = sessionmaker(bind=self.conn.engine)()
        self.conn.base.metadata.create_all(self.conn.engine)

        self.conn.add(CourseList(name="Python 100", key="p100"))
        self.conn.add(CourseList(name="Python 111", key="p111"))
        self.conn.add(CourseList(name="Python 200", key="p200"))

        self.conn.add(CourseTask(name="Python вывыести \n $", task="*", res="*", course_id=1))
        self.conn.add(CourseTask(name="Python вывыести лесенку", task="Вывести\n*\n**\n***", res="*\n**\n***",
                                 course_id=2))
        self.conn.add(CourseTask(name="Python вывыести \n !", task="*", res="*", course_id=2))
        self.conn.add(CourseTask(name="Python вывыести \n %", task="*", res="*", course_id=3))

        self.conn.add(User(id=0, fio="test"))
        self.conn.add(UserCourse(user_id=0, course_id=1))

        self.conn.commit()

    def get_all(self, class_type):
        return self.conn.session.query(class_type).all()

    def get_for_id(self, class_type, el_id):
        return self.conn.session.query(class_type).filter(class_type.id == el_id).first()

    def user_add(self, user):
        self.conn.add(User(
            id=user["id"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            username=user["username"]
        ))
        self.conn.commit()

    def task_add(self, user_id, task_id, user_task):
        for i in self.get_all(UserTask):
            if i.user_id == user_id and i.task_id == task_id:
                i.user_task = user_task
                self.conn.commit()
                return
        self.conn.add(UserTask(user_id=user_id, task_id=task_id, user_task=user_task))
        self.conn.commit()

    def user_edit_fio(self, user_id, fio):
        user = self.conn.session.query(User).filter(User.id == user_id).first()
        user.fio = fio
        self.conn.commit()

    def user_course_add(self, user_id, course_id):
        for i in self.user_course_get4id(user_id):
            if i.course_id == course_id:
                return
        self.conn.add(UserCourse(user_id=user_id, course_id=course_id))
        self.conn.commit()

    def user_course_key_check(self, key):
        course = self.conn.session.query(CourseList).filter(CourseList.key == key).first()
        if course is not None:
            course = course.id
        return course

    def user_course_get4id(self, user_id):
        return self.conn.session.query(UserCourse).filter(UserCourse.user_id == user_id).all()

    def task_get4id_course(self, course_id):
        return self.conn.session.query(CourseTask).filter(CourseTask.course_id == course_id).all()


if __name__ == "__main__":
    db = SQLAss("conf_sql.json", Base)
    db.start_build()
