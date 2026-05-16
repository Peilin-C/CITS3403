import unittest
from app import create_app, db
from app.models import User, StudySession

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
        }, follow_redirects=True)
        self.client.get('/logout', follow_redirects=True)
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

    def test_create_session_saves_to_db(self):
        self.client.post('/signup', data={
            'name': 'Test User',
            'email': 'session@uwa.edu.au',
            'password': 'Password123',
            'confirm': 'Password123'
        }, follow_redirects=True)
        self.client.post('/create_session', data={
            'name': 'CITS3403 Study',
            'unit': 'CITS3403',
            'date': '2026-06-01',
            'time': '14:00',
            'location': 'Library',
            'mode': 'In Person',
            'max_participants': '6'
        }, follow_redirects=True)
        with self.app.app_context():
            session = StudySession.query.filter_by(unit='CITS3403').first()
            self.assertIsNotNone(session)
            self.assertEqual(session.title, 'CITS3403 Study')

    def test_edit_profile_updates_db(self):
        self.client.post('/signup', data={
            'name': 'Test User',
            'email': 'edit@uwa.edu.au',
            'password': 'Password123',
            'confirm': 'Password123'
        }, follow_redirects=True)
        self.client.post('/edit_profile', data={
            'name': 'Updated Name',
            'degree': 'Computer Science',
            'units': 'CITS3403',
            'availability': 'Mornings',
            'study_style': 'Group study',
            'study_preferences': 'Library',
            'open_to_teams': 'yes'
        }, follow_redirects=True)
        with self.app.app_context():
            user = User.query.filter_by(email='edit@uwa.edu.au').first()
            self.assertEqual(user.units, 'CITS3403')
            self.assertEqual(user.study_style, 'Group study')

    def test_duplicate_email_rejected(self):
        self.client.post('/signup', data={
            'name': 'Test User',
            'email': 'duplicate@uwa.edu.au',
            'password': 'Password123',
            'confirm': 'Password123'
        }, follow_redirects=True)
        self.client.get('/logout', follow_redirects=True)
        response = self.client.post('/signup', data={
            'name': 'Another User',
            'email': 'duplicate@uwa.edu.au',
            'password': 'Password123',
            'confirm': 'Password123'
        }, follow_redirects=True)
        self.assertIn(b'already registered', response.data)

if __name__ == '__main__':
    unittest.main()