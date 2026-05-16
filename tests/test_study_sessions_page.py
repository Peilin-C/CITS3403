"""
Selenium tests for Study Sessions page.
Run with: python -m pytest tests/test_study_sessions_page.py -v
Requires Flask running on http://127.0.0.1:5000
"""
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = 'http://127.0.0.1:5000'


class StudySessionsPageTests(unittest.TestCase):

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
        cls.test_email = f'sessions_{timestamp}@student.uwa.edu.au'

        # Signup
        cls.driver.get(f'{BASE_URL}/signup')
        time.sleep(1)
        cls.driver.find_element(By.NAME, 'name').send_keys('Sessions Tester')
        cls.driver.find_element(By.NAME, 'email').send_keys(cls.test_email)
        cls.driver.find_element(By.NAME, 'password').send_keys('TestPass123')
        cls.driver.find_element(By.NAME, 'confirm').send_keys('TestPass123')
        cls.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_sessions_page_opens(self):
        """Study sessions page should load after login."""
        self.driver.get(f'{BASE_URL}/sessions')
        time.sleep(1)
        self.assertNotIn('login', self.driver.current_url.lower())
        body = self.driver.find_element(By.TAG_NAME, 'body').text.lower()
        self.assertTrue(
            'session' in body or 'study' in body,
            'Page should contain sessions content'
        )

    def test_sessions_page_has_content(self):
        """Sessions page should display session cards or empty state message."""
        self.driver.get(f'{BASE_URL}/sessions')
        time.sleep(1)
        body = self.driver.find_element(By.TAG_NAME, 'body').text
        # Page should have either session cards or a message
        cards = self.driver.find_elements(By.CSS_SELECTOR, '.card, .session-card')
        has_content = len(cards) > 0 or len(body) > 100
        self.assertTrue(has_content, 'Sessions page should have content')


if __name__ == '__main__':
    unittest.main()
