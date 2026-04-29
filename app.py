from flask import Flask, render_template
from models import db, bcrypt

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)

    # Import blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.lecturer import lecturer_bp
    from routes.student import student_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(lecturer_bp)
    app.register_blueprint(student_bp)

    @app.route('/')
    def home():
        return render_template("home.html")
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

    