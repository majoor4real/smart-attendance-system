from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime
import uuid

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Department {self.name}>"


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(150), nullable=False)

    department_id = db.Column(
        db.Integer,
        db.ForeignKey('department.id'),
        nullable=False
    )

    department = db.relationship('Department', backref='courses')

    def __repr__(self):
        return f"<Course {self.code}>"


student_courses = db.Table(
    'student_courses',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)



class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matric_no = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

    department = db.relationship('Department', backref='students')
    user = db.relationship('User', backref='student_profile')

    courses = db.relationship(
        'Course',
        secondary=student_courses,
        backref='students'
    )

    def __repr__(self):
        return f"<Student {self.matric_no}>"


class Lecturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    department = db.relationship('Department', backref='lecturers')
    user = db.relationship('User', backref='lecturer_profile')

class AttendanceSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    course = db.relationship('Course', backref='attendance_sessions')
    lecturer = db.relationship('User', backref='attendance_sessions')


class AttendanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('attendance_session.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    student = db.relationship('Student', backref='attendance_records')
    session = db.relationship('AttendanceSession', backref='attendance_records')