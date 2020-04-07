from datetime import timedelta
from users import *

# / imports

# !!!!!!! table "user", DB_PATH, Base and all modules imported from user.py !!!!!!

# !!!!!!!!!! CHECK IDS IN DATABASES BEFORE FIND !!!!!!!!!!!!!!!!

class Athlete(Base):
    __tablename__ = 'athelete'
    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.DATE)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)


def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def dif_calc(user, athlete):
    """calculate differences between user and athletes age and height
    return athlete with closest height (1rst) and athlete with closest dob (2nd)"""
    # differences between age and height by default:
    age_diff = abs(athlete[int(round(len(athlete)/2, 0))].birthdate - user.birthdate)
    height_diff = 100.0
    # closest_ for return, bu default User
    closest_height = user
    closest_age = user
    # check for correct users height and birthdate (not Null)
    if user.height and user.birthdate:
        for person in athlete:
            # check for correct athletes height and birthdate (not Null)
            if person.height and person.birthdate:
                height_diff_obj = abs(person.height - user.height)
                age_diff_obj = abs(person.birthdate - user.birthdate)
                if height_diff_obj < height_diff:
                    height_diff = height_diff_obj
                    closest_height = person
                if age_diff_obj < age_diff:
                    age_diff = age_diff_obj
                    closest_age = person
    return closest_height, closest_age


def find(id, session):

    qu = session.query(User).filter(User.id == id).first()
    if qu:
        print(f'USER ID {qu.id}, NAME {qu.first_name}, LAST_NAME {qu.last_name}, DOB {qu.birthdate}, HEIGHT {qu.height}')
        qa = session.query(Athlete).all()
        height, age = dif_calc(qu, qa)
        return height, age




def main():
    session = connect_db()
    try:
        id_to_find = int(input('ID for compare: '))
        height, dob = find(id_to_find, session)
        print(f'Athlete closest in AGE ID {dob.id}, NAME {dob.name}, DOB {dob.birthdate}')
        print(f'Athlete closest in HEIGHT ID {height.id}, NAME {height.name}, HEIGHT {height.height}')
    except (TypeError, ValueError):
        print("No such ID!")



if __name__ == '__main__':
    main()