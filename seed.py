import random
from faker import Faker
from sqlalchemy.orm import sessionmaker
from tables import Base, Student, Group, Teacher, Subject, Grade, engine

fake = Faker()

Session = sessionmaker(bind=engine)
session = Session()

num_students = 50
num_groups = 3
num_subjects = 8
num_teachers = 5

groups = [Group(name=f'Group-{i+1}') for i in range(num_groups)]
session.add_all(groups)
session.commit()

teachers = [Teacher(name=fake.name()) for _ in range(num_teachers)]
session.add_all(teachers)
session.commit()

subjects = [Subject(name=fake.word(), teacher=random.choice(teachers)) for _ in range(num_subjects)]
session.add_all(subjects)
session.commit()

for _ in range(num_students):
    student = Student(name=fake.name())
    session.add(student)

    student.group = random.choice(groups)

    for subject in subjects:
        grade = Grade(student_id=student.id, subject_id=subject.id, grade=random.randint(1, 100), date=fake.date_between(start_date='-1y'))

        session.add(grade)

session.commit()
session.close()
