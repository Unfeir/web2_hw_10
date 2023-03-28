from contextlib import contextmanager
from datetime import datetime
from random import randint, choice
from typing import List, Tuple, SupportsInt

import faker
from psycopg2 import connect, DatabaseError, Error



#
# @contextmanager
# def connection():
#     conn = None
#     try:
#         conn = connect(host='localhost', user='postgres', database='postgres', password='qwerty')
#         yield conn
#     except DatabaseError as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()
#

STUDENTS = randint(30, 50)
GROUPS = 3
TEACHERS = randint(3, 5)
SUBJECTS = randint(5, 8)
N2W = {1: 'First', 2: 'Second', 3: 'Third'}

def fake_data(students: int, groups: int, teachers: int, subjects: int)-> List:

    fake_data = faker.Faker('uk-UA')

    fake_students = [fake_data.name() for _ in range(students)]
    fake_groups = [f'{N2W.get(el + 1)} group' for el in range(groups)]
    fake_teachers = [fake_data.name() for _ in range(teachers)]
    fake_subjects = [f'факультет - {fake_data.country()} знавства' for _ in range(subjects)]

    return fake_students, fake_groups, fake_teachers, fake_subjects


def data_to_insert(students: list, groups: list, teachers: list, subjects: list)-> List:

    for_students = [(student, randint(1, GROUPS)) for student in students]
    for_groups = [(group,) for group in groups]
    for_teachers = [(teacher,) for teacher in teachers]
    for_subjects = [(subject, randint(1, TEACHERS)) for subject in subjects]
    for_grades = []
    for student_id in range(1, STUDENTS + 1):
        for _ in range(randint(15, 20)):
            date = datetime(year=2023, month=1, day=(randint(1, 31))).date()
            for_grades.append((student_id, randint(1, SUBJECTS), randint(1, 12), date))

    return for_students, for_groups, for_teachers, for_subjects, for_grades



fake_students, fake_groups, fake_teachers, fake_subjects = fake_data(STUDENTS, GROUPS, TEACHERS, SUBJECTS)
for_students, for_groups, for_teachers, for_subjects, for_grades = data_to_insert(fake_students, fake_groups, fake_teachers, fake_subjects)
print(for_groups)
# sql_groups = """INSERT INTO groups(group_name)
#                         VALUES (%s)"""
# sql_students = """INSERT INTO students(student_name, group_id)
#                                VALUES (%s, %s)"""
# sql_teachers = """INSERT INTO teachers(teacher_name)
#                             VALUES (%s)"""
# sql_subjects = """INSERT INTO subjects(subject_name, teacher_id)
#                                 VALUES (%s, %s)"""
# sql_grades = """INSERT INTO grades(student_id, subject_id, grade, grade_date)
#                                 VALUES (%s, %s, %s, %s)"""
#
# insert_data(con, sql_groups, for_groups)
# insert_data(con, sql_students, for_students)
# insert_data(con, sql_teachers, for_teachers)
# insert_data(con, sql_subjects, for_subjects)
# insert_data(con, sql_grades, for_grades)