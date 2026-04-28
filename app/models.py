from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    degree = db.Column(db.String(100))
    units = db.Column(db.String(200))
    availability = db.Column(db.String(200))
    study_style = db.Column(db.String(100))
    study_preferences = db.Column(db.String(500))
    open_to_teams = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class StudySession(db.Model):
    __tablename__ = 'study_session'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50))
    time = db.Column(db.String(20))
    location = db.Column(db.String(200))
    mode = db.Column(db.String(50))
    max_spots = db.Column(db.Integer, default=6)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship('User', backref='sessions')

    def __repr__(self):
        return f'<StudySession {self.title}>'