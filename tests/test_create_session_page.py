"""
Selenium tests for Create Session page.
Run with: python -m pytest tests/test_create_session_page.py -v
Requires Flask running on http://127.0.0.1:5000
"""
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = 'http://127.0.0.1:5000'


class CreateSessionPageTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(3)

        # Clean state
        cls.driver.get(f'{BASE_URL}/logout')
        time.sleep(1)
        cls.driver.delete_all_cookies()

        timestamp = str(int(time.time()))
        cls.test_email = f'session_{timestamp}@student.uwa.edu.au'

        # Signup
        cls.driver.get(f'{BASE_URL}/signup')
        time.sleep(1)
        cls.driver.find_element(By.NAME, 'name').send_keys('Session Tester')
        cls.driver.find_element(By.NAME, 'email').send_keys(cls.test_email)
        cls.driver.find_element(By.NAME, 'password').send_keys('TestPass123')
        cls.driver.find_element(By.NAME, 'confirm').send_keys('TestPass123')
        cls.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_create_session_page_opens(self):
        """Create session page should load after login."""
        self.driver.get(f'{BASE_URL}/create_session')
        time.sleep(1)
        self.assertNotIn('login', self.driver.current_url.lower())
        body = self.driver.find_element(By.TAG_NAME, 'body').text.lower()
        self.assertTrue(
            'create' in body or 'session' in body,
            'Page should contain create session content'
        )

    def test_create_session_has_form(self):
        """Create session page should have a form."""
        self.driver.get(f'{BASE_URL}/create_session')
        time.sleep(1)
        forms = self.driver.find_elements(By.TAG_NAME, 'form')
        self.assertTrue(len(forms) > 0, 'Create session page should have a form')


if __name__ == '__main__':
    unittest.main()
