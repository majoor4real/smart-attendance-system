from flask import Flask
from models import db, bcrypt  # make sure this is exact

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)

    # Blueprints
    from routes.auth import auth
    from routes.admin import admin_bp
    from routes.student import student_bp
    from routes.lecturer import lecturer_bp


    app.register_blueprint(auth)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(lecturer_bp)

    @app.route('/')
    def home():
        return "Smart Attendance System is running!"
    

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
