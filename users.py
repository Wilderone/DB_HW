import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# / imports

# Database should locate in project folder, change DB_PATH if not
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    birthdate = sa.Column(sa.DATE)
    height = sa.Column(sa.INTEGER)


def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def check_dob():
    """CHECK FOR RIGHT DOB FORMAT"""
    while True:
        try:
            dob_correct = datetime.strptime(input("Date of birth DD.MM.YYYY: "), '%d.%m.%Y')
        except ValueError:
            print('use DD.MM.YYYY format!')
        else:
            return dob_correct


def request_data():
    print("Fill data")
    first_name = input("First name: ").capitalize()
    last_name = input("Last name: ").capitalize()
    gender = input("Gender: ").capitalize()
    dob = check_dob()
    height = input("height: ")
    try:
        int(height)
    except ValueError:
        height = float(height)
    else:
        height = float('{:.2f}'.format(int(height)/100))

    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        birthdate=dob,
        height=height
    )
    return user


def write_data():
    session = connect_db()
    new_user = request_data()
    session.add(new_user)
    session.commit()
    print("Data saved")


if __name__ == '__main__':
    write_data()
