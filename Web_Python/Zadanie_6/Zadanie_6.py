from faker import Faker
import random
import sqlite3

fake = Faker()

conn = sqlite3.connect('students_database.db')
c = conn.cursor()


c.execute('''CREATE TABLE Students (
                student_id INTEGER PRIMARY KEY,
                name TEXT,
                group_id INTEGER)''')

c.execute('''CREATE TABLE Groups (
                group_id INTEGER PRIMARY KEY,
                name TEXT)''')

c.execute('''CREATE TABLE Lecturers (
                lecturer_id INTEGER PRIMARY KEY,
                name TEXT)''')

c.execute('''CREATE TABLE Subjects (
                subject_id INTEGER PRIMARY KEY,
                name TEXT,
                lecturer_id INTEGER,
                FOREIGN KEY (lecturer_id) REFERENCES Lecturers(lecturer_id))''')

c.execute('''CREATE TABLE Grades (
                grade_id INTEGER PRIMARY KEY,
                student_id INTEGER,
                subject_id INTEGER,
                grade REAL,
                date TEXT,
                FOREIGN KEY (student_id) REFERENCES Students(student_id),
                FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id))''')

groups = [('Group A',), ('Group B',), ('Group C',)]
c.executemany('INSERT INTO Groups (name) VALUES (?)', groups)

lecturers = [(fake.name(),) for _ in range(5)]
c.executemany('INSERT INTO Lecturers (name) VALUES (?)', lecturers)

subjects = [(fake.word(), random.randint(1, 5)) for _ in range(8)]
c.executemany('INSERT INTO Subjects (name, lecturer_id) VALUES (?, ?)', subjects)

students = [(fake.name(), random.randint(1, 3)) for _ in range(30)]
c.executemany('INSERT INTO Students (name, group_id) VALUES (?, ?)', students)

grades = [(random.randint(1, 30), random.randint(1, 8), round(random.uniform(2, 5), 2), fake.date_between(start_date='-1y', end_date='today')) for _ in range(300)]
c.executemany('INSERT INTO Grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, ?)', grades)

conn.commit()
conn.close()