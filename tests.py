import unittest
from app import create_app, db
from app.models import User

class TestStudyBuddy(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_signup_creates_user(self):
        response = self.client.post('/signup', data={
            'name': 'Test User',
            'email': 'test@uwa.edu.au',
            'password': 'Password123',
            'confirm': 'Password123'
        }, follow_redirects=True)
        with self.app.app_context():
            user = User.query.filter_by(email='test@uwa.edu.au').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.name, 'Test User')

    def test_password_is_hashed(self):
        with self.app.app_context():
            user = User(name='Test', email='hash@uwa.edu.au')
            user.set_password('Password123')
            db.session.add(user)
            db.session.commit()
            self.assertNotEqual(user.password_hash, 'Password123')
            self.assertTrue(user.check_password('Password123'))

    def test_login_with_correct_credentials(self):
        self.client.post('/signup', data={
            'name': 'Test User',
            'email': 'login@uwa.edu.au',
            'password': 'Password123',
            'confirm': 'Password123'
        })
        response = self.client.post('/login', data={
            'email': 'login@uwa.edu.au',
            'password': 'Password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_with_wrong_password(self):
        self.client.post('/signup', data={
            'name': 'Test User',
            'email': 'wrong@uwa.edu.au',
            'password': 'Password123',
            'confirm': 'Password123'
        })
        response = self.client.post('/login', data={
            'email': 'wrong@uwa.edu.au',
            'password': 'WrongPassword'
        }, follow_redirects=True)
        self.assertIn(b'Incorrect', response.data)

    def test_browse_requires_login(self):
        response = self.client.get('/browse', follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_profile_requires_login(self):
        response = self.client.get('/profile', follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_user_model_fields(self):
        with self.app.app_context():
            user = User(
                name='Aisha Khan',
                email='aisha@uwa.edu.au',
                units='CITS3403',
                availability='Tuesday afternoons',
                study_style='Group study',
                open_to_teams=True
            )
            user.set_password('Password123')
            db.session.add(user)
            db.session.commit()
            saved = User.query.filter_by(email='aisha@uwa.edu.au').first()
            self.assertEqual(saved.units, 'CITS3403')
            self.assertEqual(saved.study_style, 'Group study')
            self.assertTrue(saved.open_to_teams)

if __name__ == '__main__':
    unittest.main()
