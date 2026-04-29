from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from models import db, User, Department, Course, Lecturer

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ------------------ Admin Dashboard ------------------
@admin_bp.route('/')
def admin_dashboard():
    if 'user_id' not in session:
        flash("Please login first")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    department_count = Department.query.count()
    course_count = Course.query.count()
    user_count = User.query.count()

    return render_template(
        'admin_dashboard.html',
        display_name=user.username,
        role=user.role,
        department_count=department_count,
        course_count=course_count,
        user_count=user_count
    )

# ------------------ Register Lecturer ------------------
@admin_bp.route('/register-lecturer', methods=['GET', 'POST'])
def register_lecturer():
    if 'user_id' not in session:
        flash("Please login first")
        return redirect(url_for('auth.login'))
    if session.get('role') != 'admin':
        flash("Access denied")
        return redirect(url_for('auth.login'))

    departments = Department.query.all()
    lecturer_users = User.query.filter_by(role='lecturer').all()

    if request.method == 'POST':
        full_name = request.form['full_name'].strip()
        department_id = request.form['department_id']
        user_id = request.form['user_id']

        existing_link = Lecturer.query.filter_by(user_id=user_id).first()
        if existing_link:
            flash("This lecturer user account is already linked")
            return redirect(url_for('admin.register_lecturer'))

        lecturer = Lecturer(full_name=full_name, department_id=department_id, user_id=user_id)
        db.session.add(lecturer)
        db.session.commit()

        flash("Lecturer registered successfully")
        return redirect(url_for('admin.register_lecturer'))

    lecturers = Lecturer.query.all()
    return render_template(
        "lecturer_register.html",
        departments=departments,
        lecturers=lecturers,
        lecturer_users=lecturer_users
    )

# ------------------ Manage Users ------------------
@admin_bp.route('/manage-users', methods=['GET', 'POST'])
def manage_users():
    if 'user_id' not in session:
        flash("Please login first")
        return redirect(url_for('auth.login'))
    if session.get('role') != 'admin':
        flash("Access denied")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        role = request.form['role']

        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            return redirect(url_for('admin.manage_users'))

        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("User account created successfully")
        return redirect(url_for('admin.manage_users'))

    users = User.query.all()
    return render_template("manage_users.html", users=users)

# ------------------ Manage Departments ------------------
@admin_bp.route('/manage-departments', methods=['GET', 'POST'])
def manage_departments():
    if 'user_id' not in session:
        flash("Please login first")
        return redirect(url_for('auth.login'))
    if session.get('role') != 'admin':
        flash("Access denied")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        department_name = request.form['department_name'].strip()
        if Department.query.filter_by(name=department_name).first():
            flash("Department already exists")
            return redirect(url_for('admin.manage_departments'))

        new_dept = Department(name=department_name)
        db.session.add(new_dept)
        db.session.commit()

        flash("Department added successfully")
        return redirect(url_for('admin.manage_departments'))

    departments = Department.query.all()
    return render_template("manage_departments.html", departments=departments)
    
# ------------------ Manage Lecturers ------------------
@admin_bp.route('/manage-lecturers', methods=['GET', 'POST'])
def manage_lecturers():
    if 'user_id' not in session:
        flash("Please login first")
        return redirect(url_for('auth.login'))
    if session.get('role') != 'admin':
        flash("Access denied")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        full_name = request.form['full_name'].strip()
        department_id = request.form['department_id']
        user_id = request.form['user_id']

        # Check if this user is already a lecturer
        if Lecturer.query.filter_by(user_id=user_id).first():
            flash("This user is already registered as a lecturer")
            return redirect(url_for('admin.manage_lecturers'))

        lecturer = Lecturer(full_name=full_name, department_id=department_id, user_id=user_id)
        db.session.add(lecturer)
        db.session.commit()
        flash("Lecturer added successfully")
        return redirect(url_for('admin.manage_lecturers'))

    departments = Department.query.all()
    lecturer_users = User.query.filter_by(role='lecturer').all()
    lecturers = Lecturer.query.all()

    return render_template(
        "manage_lecturers.html",
        departments=departments,
        lecturer_users=lecturer_users,
        lecturers=lecturers
    )


# ------------------ Manage Courses ------------------
@admin_bp.route('/manage-courses', methods=['GET', 'POST'])
def manage_courses():
    if 'user_id' not in session:
        flash("Please login first")
        return redirect(url_for('auth.login'))
    if session.get('role') != 'admin':
        flash("Access denied")
        return redirect(url_for('auth.login'))

    departments = Department.query.all()

    if request.method == 'POST':
        code = request.form['code'].strip().upper()
        title = request.form['title'].strip()
        department_id = request.form['department_id']

        existing_course = Course.query.filter_by(code=code).first()
        if existing_course:
            flash("Course code already exists")
            return redirect(url_for('admin.manage_courses'))

        new_course = Course(
            code=code,
            title=title,
            department_id=department_id
        )

        db.session.add(new_course)
        db.session.commit()

        flash("Course added successfully")
        return redirect(url_for('admin.manage_courses'))

    courses = Course.query.all()
    return render_template(
        "manage_courses.html",
        courses=courses,
        departments=departments
    )