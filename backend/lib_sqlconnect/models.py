from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

Base = declarative_base()


class StudentCourse(Base):
    """Описывает таблицу с курсами на которые записан студент"""
    __tablename__ = "student_course"                                            # имя таблицы
    id = Column(Integer, primary_key=True)                                      # id в базе, автоинкриментируемое
    student_id = Column(Integer, ForeignKey("student.id", ondelete='CASCADE'))  # id студента (которому принадлежит курс)
    course_id = Column(Integer, ForeignKey("course.id", ondelete='CASCADE'))    # id курса в базе (на который записан студент)

    course = relationship("Course", back_populates="student_course")
    student = relationship("Student", back_populates="student_course")

    def __repr__(self):
        return f"""<UserCourse(
                        id={self.id}, 
                        student_id='{self.student_id}', 
                        course_id='{self.course_id}'
                    )>"""


class StudentTask(Base):
    """Описывает таблицу с заданиями которые выполнили студенты"""
    __tablename__ = "student_task"                                               # имя таблицы
    id = Column(Integer, primary_key=True)                                       # id в базе, автоинкриментируемое
    student_id = Column(Integer, ForeignKey("student.id", ondelete='CASCADE'))   # id студента выполневшего задание
    task_id = Column(Integer, ForeignKey("course_task.id", ondelete='CASCADE'))  # id задания, которое выполнил студент
    student_task = Column(String)                                                # текст задания
    res = Column(String)                                                         # текст результата
    log = Column(String)                                                         # лог проверки
    flag = Column(Integer)                                                       # флаг проверки

    student = relationship("Student", back_populates="student_task")
    course_task = relationship("CourseTask", back_populates="student_task")

    # Флаг проверки
    # 1 - проверка пройдена успешна результат положительный,
    # 2 - проверка пройдена успешно результат отрецательный,
    # 3 - проверка провалена, результат в логах ошибки

    def __repr__(self):
        return f"""<StudentTask(
                    id={self.id}, 
                    student_id='{self.student_id}', 
                    task_id='{self.task_id}',            
                    student_task='{self.student_task}',
                    res='{self.res}',
                    log='{self.log}',
                    flag='{self.flag}'
                )>"""


class Student(Base):
    """Описывает таблицу со студентами курса"""
    __tablename__ = "student"               # имя таблицы
    id = Column(Integer, primary_key=True)  # id в базе (взято из телеграмма)
    fio = Column(String)                    # Ф.И.О введенное студентом
    first_name = Column(String)             # Имя взятое из телеграмма при регистрации
    last_name = Column(String)              # Фамилия взятая из телеграмма при регистрации
    username = Column(String)               # Короткое имя взятое из телеграмма (пишется после @)
    status = Column(Boolean, default=True)

    student_course = relationship("StudentCourse", back_populates="student", cascade="all, delete", passive_deletes=True)
    student_task = relationship("StudentTask", back_populates="student", cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return f"""<Student(
                        id={self.id}, 
                        fio='{self.fio}',
                        first_name='{self.first_name}, 
                        last_name='{self.last_name}', 
                        username='{self.username}
                    )>"""


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    status = Column(Boolean, default=True)
    position = Column(Integer, nullable=True)
    username = Column(String)
    password = Column(String)

    def json(self):
        return {'id': self.id,
                'first_name': self.first_name,
                'middle_name': self.middle_name,
                'last_name': self.last_name,
                'status': self.status,
                'position': self.position,
                'username': self.username,
                'password': self.password
                }

    def __repr__(self):                                             # дописать __repr__
        return f"""<User(
                            id={self.id}, 
                            first_name='{self.first_name}', 
                            middle_name='{self.middle_name}',            
                            last_name='{self.last_name}',
                            status='{self.status}',
                            position='{self.position}',
                            password='{self.password}'
                        )>"""


class CourseTask(Base):
    """Описывает таблицу содержащую задания для курсов"""
    __tablename__ = "course_task"                                                # имя таблицы
    id = Column(Integer, primary_key=True)                                       # id в базе, автоинкриментируемое
    name = Column(String)                                                        # Название задания
    course_id = Column(Integer, ForeignKey("course.id", ondelete='CASCADE'))     # id курса которому принадлежит задание
    task = Column(String)                                    # задание
    flag = Column(Integer)                                   # флаг указываещий на тип проверки
    res = Column(String)                                     # ожидаемый результат / текст файла для тестирования кода

    course = relationship("Course", back_populates="course_task")
    student_task = relationship("StudentTask", back_populates="course_task", cascade="all, delete", passive_deletes=True)

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'course_id': self.course_id,
                'task': self.task,
                'flag': self.flag,
                'res': self.res,
                }

    def __repr__(self):
        return f"""<CourseTask(
                        id={self.id}, 
                        name='{self.name}', 
                        course_id='{self.course_id}',
                        task='{self.task}', 
                        flag='{self.flag}', 
                        res='{self.res}'
                    )>"""


class Course(Base):
    """Описывает таблицу курсами зарегистрированными в системе"""
    __tablename__ = "course"  # имя таблицы
    id = Column(Integer, primary_key=True)                    # id в базе, автоинкриментируемое
    name = Column(String)                                     # название курса
    slug_name = Column(String)                                # user-friendly название курса в адресной строке
    key = Column(String)                                      # ключ неоходимый для добавления студенту курса

    course_task = relationship("CourseTask", back_populates="course", cascade="all, delete", passive_deletes=True)
    student_course = relationship("StudentCourse", back_populates="course", cascade="all, delete", passive_deletes=True)

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'key': self.key,
                'slug_name': self.slug_name}

    def __repr__(self):
        return f"""<Course(
                        id={self.id}, 
                        name='{self.name}', 
                        key='{self.key}'
                    )>"""
