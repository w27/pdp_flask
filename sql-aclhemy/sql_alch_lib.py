from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker



Base = declarative_base()

class User(Base):
    __tablename__ = "test_user_list"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    ip = Column(String)

    def __repr__(self):
        return f"user id:{self.id}, name:{self.name}, password:{self.password}, ip:{self.ip}"




my_engine = create_engine(f'postgresql+psycopg2://',
                                    echo=False)
my_session = sessionmaker(bind=my_engine)()

Base.metadata.create_all(my_engine)  # создание новых таблиц, это делать не надо

# user = User(name="Вася", password="1", ip="111.111.11.111")

# my_session.add(user)

# print('Test', user)
#
my_session.commit()  # "применить изменения в таблице"
#
# print(user)
#
# user.name = 'Петя'

# print(user)

# my_session.commit()
#
# pop_user = my_session.query(User).all()
# pop_user[0].name = "ggg"
# print(type(pop_user[0]))
# my_session.commit()
#
#
# print(pop_user)
#
# print("string")
#
#
#
# t = my_session.query(User).filter(User.id == 5).first()
#
# t.name = "маруся"
#
# my_session.commit()
#
#
#
# print(t)


def create_user(name, password, ip):
    if my_session.query(User).filter(User.name==name).first():
        print("Это имя уже занято")
        return
    user = User(name=name, password=password, ip=ip)
    my_session.add(user)
    my_session.commit()


create_user('FFF', 'fkf', 'jhb')
create_user("Вася", "12345", "100.10.100.100")
create_user("Петя", "6789", "200.20.200.200")
