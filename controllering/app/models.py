from app import db

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    