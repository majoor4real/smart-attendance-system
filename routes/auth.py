from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User
from sqlalchemy import func

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        user = User.query.filter(func.lower(User.username) == username.lower()).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['role'] = user.role

            if user.role == 'admin':
                return redirect(url_for('admin.admin_dashboard'))

            elif user.role == 'lecturer':
                return redirect(url_for('lecturer.lecturer_dashboard'))

            elif user.role == 'student':
                return redirect(url_for('student.student_dashboard'))

        flash("Invalid username or password")
        return redirect(url_for('auth.login'))

    return render_template('login.html')


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        matric_no = request.form['matric_no'].strip().upper()
        password = request.form['password'].strip()
        confirm_password = request.form['confirm_password'].strip()

        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for('auth.signup'))

        existing_user = User.query.filter_by(username=matric_no).first()
        if existing_user:
            flash("Matric number already exists")
            return redirect(url_for('auth.signup'))

        user = User(username=matric_no, role='student')
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully! Please login.")
        return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out")
    return redirect(url_for('auth.login'))