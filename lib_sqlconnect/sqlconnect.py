from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib_sqlconnect import Base, Course, CourseTask, User
import lib_sqlconnect.config as conf


class SQLConnect:
    def __init__(self):
        self.base = Base
        self.engine = create_engine("sqlite:///test.sqlite")

        self._start_session()

    def metadata_upgrade(self):
        self.base.metadata.create_all(self.engine)

    def _start_session(self):
        self.session = sessionmaker(bind=self.engine)()

    def clean_db(self):
        self.session.close()
        self.base.metadata.drop_all(self.engine)
        self._start_session()

    def add(self, obj):
        self.session.add(obj)
    
    def delete(self, obj):
        self.session.delete(obj)

    def commit(self):
        self.session.commit()

    def get(self, class_type, class_attribute=None, attribute_value=None, one=False):
        if class_attribute is None:
            return self.session.query(class_type).all()
        if one:
            return self.session.query(class_type).filter(class_type.__dict__.get(class_attribute) == attribute_value).first()
        return self.session.query(class_type).filter(class_type.__dict__.get(class_attribute) == attribute_value).all()


def start_build():
    conn = SQLConnect()
    conn.clean_db()

    conn.metadata_upgrade()

    conn.add(Course(name="Python 100", key="p100", slug_name="py-100"))
    conn.add(Course(name="Python 111", key="p111", slug_name="py-111"))
    conn.add(Course(name="Python 200", key="p200", slug_name="py-200"))

    conn.add(CourseTask(name="Python вывыести \n *", task="*", res="*", course_id=1))
    conn.add(CourseTask(name="Python вывыести лесенку", task="Вывести\n*\n**\n***", res="*\n**\n***",
                             course_id=2))
    conn.add(CourseTask(name="Python вывыести \n !", task="!", res="!", course_id=2))
    conn.add(CourseTask(name="Python вывыести \n %", task="%", res="%", course_id=3))
    conn.add(User(username="dima", password="1234"))

    conn.commit()


if __name__ == "__main__":
    # start_build()
    s = SQLConnect()

