"""
Unit tests for authentication (login, signup, logout).
Run with: python -m pytest tests/test_auth.py -v
"""
import unittest
from app import create_app, db
from app.models import User


class AuthUnitTests(unittest.TestCase):
    """Unit tests for signup, login, and logout."""

    def setUp(self):
        """Create app, database, and test client before each test."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_signup_creates_user(self):
        response = self.client.post('/signup', data={
            'name': 'Test User',
            'email': 'test@student.uwa.edu.au',
            'password': 'Password123',
            'confirm': 'Password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(email='test@student.uwa.edu.au').first()
        self.assertIsNotNone(user)
        self.assertNotEqual(user.password_hash, 'Password123')

    def test_signup_duplicate_email(self):
        user = User(name='First', email='dup@student.uwa.edu.au')
        user.set_password('Password123')
        db.session.add(user)
        db.session.commit()
        self.client.post('/signup', data={
            'name': 'Second',
            'email': 'dup@student.uwa.edu.au',
            'password': 'Password456',
            'confirm': 'Password456'
        }, follow_redirects=True)
        users = User.query.filter_by(email='dup@student.uwa.edu.au').all()
        self.assertEqual(len(users), 1)

    def test_login_correct_password(self):
        user = User(name='Login Test', email='login@student.uwa.edu.au')
        user.set_password('CorrectPass123')
        db.session.add(user)
        db.session.commit()
        response = self.client.post('/login', data={
            'email': 'login@student.uwa.edu.au',
            'password': 'CorrectPass123'
        }, follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_login_wrong_password(self):
        user = User(name='Wrong', email='wrong@student.uwa.edu.au')
        user.set_password('RightPass123')
        db.session.add(user)
        db.session.commit()
        response = self.client.post('/login', data={
            'email': 'wrong@student.uwa.edu.au',
            'password': 'WrongPass999'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incorrect', response.data)

    def test_logout(self):
        user = User(name='Logout', email='logout@student.uwa.edu.au')
        user.set_password('Password123')
        db.session.add(user)
        db.session.commit()
        self.client.post('/login', data={
            'email': 'logout@student.uwa.edu.au',
            'password': 'Password123'
        })
        response = self.client.get('/logout', follow_redirects=False)
        self.assertIn(response.status_code, [302, 301])
        response = self.client.get('/browse', follow_redirects=False)
        self.assertIn(response.status_code, [302, 301])


if __name__ == '__main__':
    unittest.main()
