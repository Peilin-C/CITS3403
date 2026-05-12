"""
Selenium tests for authentication pages.
Run with: python -m pytest tests/test_auth_selenium.py -v
"""
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = 'http://127.0.0.1:5000'


class AuthSeleniumTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        """Logout before each test to ensure clean state."""
        self.driver.get(f'{BASE_URL}/logout')
        time.sleep(1)
        self.driver.delete_all_cookies()

    def _signup(self, name, email, password):
        self.driver.get(f'{BASE_URL}/signup')
        time.sleep(1)
        self.driver.find_element(By.NAME, 'name').send_keys(name)
        self.driver.find_element(By.NAME, 'email').send_keys(email)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.NAME, 'confirm').send_keys(password)
        self.driver.execute_script("document.querySelector('form').submit();")
        time.sleep(2)

    def _login(self, email, password):
        self.driver.get(f'{BASE_URL}/login')
        time.sleep(1)
        self.driver.find_element(By.NAME, 'email').send_keys(email)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.execute_script("document.querySelector('form').submit();")
        time.sleep(2)

    # Test 1: Signup page loads correctly
    def test_1_signup_page_loads(self):
        """Signup page should load and contain signup form."""
        self.driver.get(f'{BASE_URL}/signup')
        time.sleep(1)
        title = self.driver.title
        self.assertIn('Sign Up', title)
        form = self.driver.find_elements(By.TAG_NAME, 'form')
        self.assertTrue(len(form) > 0, 'Signup page should have a form')

    # Test 2: Signup creates account and redirects to login
    def test_2_signup_redirects_to_login(self):
        """Successful signup should redirect to login page."""
        timestamp = str(int(time.time()))
        email = f'sel_{timestamp}@student.uwa.edu.au'
        self._signup('Test User', email, 'TestPass123')
        self.assertIn('login', self.driver.current_url.lower())

    # Test 3: Login with correct credentials redirects
    def test_3_login_success(self):
        """Login with correct credentials should redirect away from login."""
        timestamp = str(int(time.time()))
        email = f'login_{timestamp}@student.uwa.edu.au'
        self._signup('Login Test', email, 'TestPass123')
        self._login(email, 'TestPass123')
        self.assertNotIn('/login', self.driver.current_url)

    # Test 4: Login with wrong password stays on login
    def test_4_login_wrong_password(self):
        """Login with wrong password should stay on login page."""
        timestamp = str(int(time.time()))
        email = f'wrong_{timestamp}@student.uwa.edu.au'
        self._signup('Wrong Test', email, 'CorrectPass123')
        self._login(email, 'WrongPass999')
        self.assertIn('login', self.driver.current_url.lower())

    # Test 5: Logout redirects to login
    def test_5_logout(self):
        """After logout, should redirect to login page."""
        timestamp = str(int(time.time()))
        email = f'out_{timestamp}@student.uwa.edu.au'
        self._signup('Logout Test', email, 'TestPass123')
        self._login(email, 'TestPass123')
        self.driver.get(f'{BASE_URL}/logout')
        time.sleep(2)
        self.assertIn('login', self.driver.current_url.lower())


if __name__ == '__main__':
    unittest.main()
