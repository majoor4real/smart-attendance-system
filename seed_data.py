from app import app
from models import db, User, Department, Course, Student, Lecturer

with app.app_context():

    # -------------------------
    # CREATE USERS
    # -------------------------
    admin = User(username='admin1', role='admin')
    admin.set_password('1234')

    lecturer_user = User(username='lecturer1', role='lecturer')
    lecturer_user.set_password('1234')

    student_user = User(username='student1', role='student')
    student_user.set_password('1234')

    db.session.add_all([admin, lecturer_user, student_user])
    db.session.commit()

    # -------------------------
    # CREATE DEPARTMENTS
    # -------------------------
    cs_department = Department(name='Computer Science')
    it_department = Department(name='Information Technology')

    db.session.add_all([cs_department, it_department])
    db.session.commit()

    # -------------------------
    # CREATE COURSES
    # -------------------------
    c1 = Course(code='CSC401', title='Software Engineering', department_id=cs_department.id)
    c2 = Course(code='CSC402', title='Database Systems', department_id=cs_department.id)
    c3 = Course(code='CSC403', title='Artificial Intelligence', department_id=cs_department.id)

    db.session.add_all([c1, c2, c3])
    db.session.commit()

    # -------------------------
    # CREATE LECTURER PROFILE
    # -------------------------
    lecturer = Lecturer(
        full_name='Dr. John Lecturer',
        user_id=lecturer_user.id,
        department_id=cs_department.id
    )

    db.session.add(lecturer)
    db.session.commit()

    # -------------------------
    # CREATE STUDENT PROFILE
    # -------------------------
    student = Student(
        matric_no='CSC/2021/001',
        full_name='Ibrahim Student',
        user_id=student_user.id,
        department_id=cs_department.id
    )

    db.session.add(student)
    db.session.commit()

    print("Sample data inserted successfully!")