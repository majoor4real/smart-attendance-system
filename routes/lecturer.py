from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models import db, User, Course, AttendanceSession, AttendanceRecord, Lecturer
import uuid
import datetime
import qrcode
import os

lecturer_bp = Blueprint('lecturer', __name__, url_prefix='/lecturer')


# ------------------ Lecturer Dashboard ------------------
@lecturer_bp.route('/')
def lecturer_dashboard():
    if 'user_id' not in session:
        flash("Please login first")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    session_count = AttendanceSession.query.filter_by(lecturer_id=user.id).count()
    course_count = Course.query.count()
    record_count = AttendanceRecord.query.join(AttendanceSession).filter(
        AttendanceSession.lecturer_id == user.id
    ).count()

    return render_template(
        'lecturer_dashboard.html',
        display_name=user.username,
        role=user.role,
        session_count=session_count,
        course_count=course_count,
        record_count=record_count
    )


# ------------------ Start Attendance ------------------
@lecturer_bp.route('/start', methods=['GET', 'POST'])
def start_attendance():
    if 'user_id' not in session:
        flash("Please login first")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    courses = Course.query.all()

    if request.method == 'POST':
        course_id = request.form['course']
        token = str(uuid.uuid4())

        end_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)

        session_record = AttendanceSession(
            course_id=course_id,
            lecturer_id=user.id,
            token=token,
            end_time=end_time
        )

        db.session.add(session_record)
        db.session.commit()

        # Create QR data
        qr_data = f"SESSION:{session_record.id}|TOKEN:{token}"

        # Generate QR
        qr = qrcode.make(qr_data)

        # Folder for QR codes
        qr_folder = os.path.join("static", "qrcodes")

        if not os.path.exists(qr_folder):
            os.makedirs(qr_folder)

        # File path
        qr_path = os.path.join(qr_folder, f"session_{session_record.id}.png")

        # Save QR
        qr.save(qr_path)

        return render_template(
            "show_qr.html",
            qr_image=f"qrcodes/session_{session_record.id}.png",
            qr_data=qr_data,
            display_name=user.username,
            role=user.role
        )

    return render_template(
        "start_attendance.html",
        courses=courses,
        display_name=user.username,
        role=user.role
    )


# ------------------ Lecturer Attendance Records ------------------
@lecturer_bp.route('/records')
def lecturer_records():
    if 'user_id' not in session:
        flash("Please login first")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    records = AttendanceRecord.query.join(AttendanceSession).filter(
        AttendanceSession.lecturer_id == user.id
    ).all()

    return render_template(
        "lecturer_records.html",
        records=records,
        display_name=user.username,
        role=user.role
    )