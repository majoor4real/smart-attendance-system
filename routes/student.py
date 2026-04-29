from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, User, Student, Course, AttendanceSession, AttendanceRecord
import datetime

student_bp = Blueprint('student', __name__, url_prefix='/student')





# ------------------ Student Dashboard ------------------
@student_bp.route('/')
def student_dashboard():
    if 'user_id' not in session:
        flash("Please login first")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    student = Student.query.filter_by(user_id=user.id).first()

    registered_course_count = len(student.courses) if student else 0
    attendance_count = len(student.attendance_records) if student else 0

    display_name = (
        student.full_name if student and student.full_name else user.username
        
    )

    return render_template(
        'student_dashboard.html',
        user=user,
        student=student,
        display_name=display_name,
        role=user.role,
        registered_course_count=registered_course_count,
        attendance_count=attendance_count

      
    )
        


# ------------------ Register Courses ------------------
@student_bp.route('/register-courses', methods=['GET', 'POST'])
def register_courses():
    if 'user_id' not in session:
        flash("Please login first")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    student = Student.query.filter_by(user_id=user.id).first()

    if not student:
        flash("Student profile not found")
        return redirect(url_for('student.student_dashboard'))

    courses = Course.query.all()

    if request.method == 'POST':
        selected_courses = request.form.getlist('courses')

        student.courses = []
        for course_id in selected_courses:
            course = Course.query.get(course_id)
            if course:
                student.courses.append(course)

        db.session.commit()
        flash("Courses registered successfully")
        return redirect(url_for('student.register_courses'))

    return render_template(
        'register_courses.html',
        student=student,
        courses=courses,
        display_name=student.full_name if student.full_name else user.username,
        role=user.role
    )


# ------------------ Scan Attendance ------------------
@student_bp.route('/scan-attendance', methods=['GET', 'POST'])
def scan_attendance():
    if 'user_id' not in session:
        flash("Please login first")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    student = Student.query.filter_by(user_id=user.id).first()

    if not student:
        flash("Student profile not found")
        return redirect(url_for('student.student_dashboard'))

    if request.method == 'POST':
        qr_data = request.form['qr_data'].strip()

        try:
            # Expected format: SESSION:1|TOKEN:xxxxx
            parts = qr_data.split('|')
            session_id = parts[0].split(':')[1]
            token = parts[1].split(':')[1]

            attendance_session = AttendanceSession.query.filter_by(
                id=session_id,
                token=token
            ).first()

            if not attendance_session:
                flash("Invalid QR code")
                return redirect(url_for('student.scan_attendance'))

            if attendance_session.end_time < datetime.datetime.utcnow():
                flash("Attendance session has expired")
                return redirect(url_for('student.scan_attendance'))

            # Prevent duplicate attendance
            existing_record = AttendanceRecord.query.filter_by(
                session_id=attendance_session.id,
                student_id=student.id
            ).first()

            if existing_record:
                flash("You have already marked attendance for this session")
                return redirect(url_for('student.scan_attendance'))

            # Optional: Ensure student registered the course
            if attendance_session.course not in student.courses:
                flash("You are not registered for this course")
                return redirect(url_for('student.scan_attendance'))

            record = AttendanceRecord(
                session_id=attendance_session.id,
                student_id=student.id
            )

            db.session.add(record)
            db.session.commit()

            flash("Attendance marked successfully")
            return redirect(url_for('student.attendance_history'))

        except Exception:
            flash("Invalid QR input format")
            return redirect(url_for('student.scan_attendance'))

    return render_template(
        'scan_attendance.html',
        display_name=student.full_name if student.full_name else user.username,
        role=user.role
    )


# ------------------ Attendance History ------------------
@student_bp.route('/attendance-history', methods=['GET', 'POST'])
#def scan_attendance():
def attendance_history():
    if 'user_id' not in session:
        flash("Please login first")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    student = Student.query.filter_by(user_id=user.id).first()

    if not student:
        flash("Student profile not found")
        return redirect(url_for('student.student_dashboard'))

    records = AttendanceRecord.query.filter_by(student_id=student.id).all()

    return render_template(
        'student_history.html',
        records=records,
        student=student,
        user=user,
        display_name=student.full_name if student.full_name else user.username,
        role=user.role
    )


# ------------------ My Courses ------------------
@student_bp.route('/my-courses')
def my_courses():
    if 'user_id' not in session:
        flash("Please login first")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    student = Student.query.filter_by(user_id=user.id).first()

    if not student:
        flash("Student profile not found")
        return redirect(url_for('student.student_dashboard'))

    print("STUDENT:", student)
    print("REGISTERED COURSES:", student.courses)

    return render_template(
        'my_courses.html',
        student=student,
        courses=student.courses,
        user=user,
        display_name=student.full_name if student.full_name else user.username,
        role=user.role
    )
    # ------------------ My Attendance Records ------------------
@student_bp.route('/my-attendance-records')
def my_attendance_records():
    if 'user_id' not in session:
        flash("Please login first")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    student = Student.query.filter_by(user_id=user.id).first()

    if not student:
        flash("Student profile not found")
        return redirect(url_for('student.student_dashboard'))

    records = AttendanceRecord.query.filter_by(student_id=student.id).all()

    return render_template(
        'my_attendance_records.html',
        student=student,
        records=records,
        user=user,
        display_name=student.full_name if student.full_name else user.username,
        role=user.role
    )

# ------------------ JAMB Practice CBT ------------------
@student_bp.route('/jamb-practice')
def jamb_practice():
    if 'user_id' not in session:
        flash("Please login first")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    student = Student.query.filter_by(user_id=user.id).first()

    return render_template(
        'jamb_mock_cbt.html',
        user=user,
        student=student,
        display_name=student.full_name if student and student.full_name else user.username,
        role=user.role
    )