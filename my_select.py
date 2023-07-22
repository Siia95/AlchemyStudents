from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from tables import engine, Student, Grade, Subject, Group, Teacher


Session = sessionmaker(bind=engine)
session = Session()


# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    result = session.query(Student, func.avg(Grade.grade).label('average_grade')).join(Grade).group_by(Student.id).order_by(
        func.avg(Grade.grade).desc()).limit(5).all()
    return result


# Знайти студента із найвищим середнім балом з певного предмета.
def select_2(subject_name):
    result = session.query(Student, func.avg(Grade.grade).label('average_grade')).join(Grade).join(Subject).filter(
        Subject.name == subject_name).group_by(Student.id).order_by(func.avg(Grade.grade).desc()).first()
    return result

# Знайти середній бал у групах з певного предмета.
def select_3(subject_name):
    result = session.query(Group, func.avg(Grade.grade).label('average_grade')).join(Student).join(Grade, Student.id == Grade.student_id).join(Subject).filter(
        Subject.name == subject_name).group_by(Group.id, Group.name).all()
    return result




# Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    result = session.query(func.avg(Grade.grade).label('average_grade')).scalar()
    return result


# Знайти, які курси читає певний викладач.
def select_5(teacher_name):
    result = session.query(Teacher).filter_by(name=teacher_name).first()
    if result:
        courses = result.subjects
        return courses
    else:
        return []


# Знайти список студентів у певній групі.
def select_6(group_name):
    result = session.query(Student).join(Group, Student.group_id == Group.id).filter(Group.name == group_name).all()
    return result


# Знайти оцінки студентів в окремій групі з певного предмета.
def select_7(group_name, subject_name):
    result = session.query(Student, Grade).join(Group).join(Grade).join(Subject).filter(Group.name == group_name,
                                                                                       Subject.name == subject_name).all()
    return result


# Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher_name):
    result = session.query(func.avg(Grade.grade).label('average_grade')).join(Subject).join(Teacher).filter(
        Teacher.name == teacher_name).scalar()
    return result if result is not None else 0


# Знайти список курсів, які відвідує певний студент.
def select_9(student_name):
    result = session.query(Student).filter_by(name=student_name).first()
    if result:
        courses = result.grades
        return courses
    else:
        return []


# Список курсів, які певному студенту читає певний викладач.
def select_10(student_name, teacher_name):
    result = session.query(Student).filter_by(name=student_name).first()
    if result:
        courses = session.query(Grade).join(Subject).join(Teacher).filter(Grade.student_id == result.id,
                                                                         Teacher.name == teacher_name).all()
        return courses
    else:
        return []


if __name__ == "__main__":
    # Приклади виклику функцій
    result1 = select_1()
    print(result1)

    result2 = select_2("Math")
    print(result2)

    result3 = select_3("History")
    print(result3)

    result4 = select_4()
    print(result4)

    result5 = select_5("John Doe")
    print(result5)

    result6 = select_6("Group-1")
    print(result6)

    result7 = select_7("Group-1", "Math")
    print(result7)

    result8 = select_8("John Doe")
    print(result8)

    result9 = select_9("Alice")
    print(result9)

    result10 = select_10("Alice", "Math")
    print(result10)
