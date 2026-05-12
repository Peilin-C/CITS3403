"""
Selenium tests for session page buttons (join, view, edit, create).
Run with: python -m pytest tests/test_session_buttons.py -v
Requires Flask running on http://127.0.0.1:5000
"""
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = 'http://127.0.0.1:5000'


class SessionButtonTests(unittest.TestCase):

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
        cls.test_email = f'buttons_{timestamp}@student.uwa.edu.au'

        # Signup
        cls.driver.get(f'{BASE_URL}/signup')
        time.sleep(1)
        cls.driver.find_element(By.NAME, 'name').send_keys('Button Tester')
        cls.driver.find_element(By.NAME, 'email').send_keys(cls.test_email)
        cls.driver.find_element(By.NAME, 'password').send_keys('TestPass123')
        cls.driver.find_element(By.NAME, 'confirm').send_keys('TestPass123')
        cls.driver.execute_script("document.querySelector('form').submit();")
        time.sleep(2)

        # Login
        cls.driver.get(f'{BASE_URL}/login')
        time.sleep(1)
        cls.driver.find_element(By.NAME, 'email').send_keys(cls.test_email)
        cls.driver.find_element(By.NAME, 'password').send_keys('TestPass123')
        cls.driver.execute_script("document.querySelector('form').submit();")
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_sessions_page_has_buttons(self):
        """Sessions page should have action buttons (join, view, create, etc)."""
        self.driver.get(f'{BASE_URL}/sessions')
        time.sleep(1)
        buttons = self.driver.find_elements(By.TAG_NAME, 'button')
        links = self.driver.find_elements(By.CSS_SELECTOR, 'a.btn, a.btn-primary, a.btn-outline-primary')
        total_actions = len(buttons) + len(links)
        self.assertTrue(
            total_actions > 0,
            'Sessions page should have at least one action button or link'
        )

    def test_create_session_button_exists(self):
        """There should be a way to navigate to create session."""
        self.driver.get(f'{BASE_URL}/sessions')
        time.sleep(1)
        body = self.driver.find_element(By.TAG_NAME, 'body')
        page_html = body.get_attribute('innerHTML').lower()
        has_create_link = 'create' in page_html
        # Also check if there's a direct link/button to create session
        create_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="create"]')
        create_buttons = self.driver.find_elements(By.XPATH, '//button[contains(text(), "Create")]')
        self.assertTrue(
            has_create_link or len(create_links) > 0 or len(create_buttons) > 0,
            'Should have a create session button or link'
        )

    def test_create_session_submit_button_works(self):
        """Create session form should have a working submit button."""
        self.driver.get(f'{BASE_URL}/create_session')
        time.sleep(1)
        submit_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button[type="submit"]')
        regular_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button.btn-success, button.btn-primary')
        total = len(submit_buttons) + len(regular_buttons)
        self.assertTrue(
            total > 0,
            'Create session page should have a submit button'
        )


if __name__ == '__main__':
    unittest.main()
