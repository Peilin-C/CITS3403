"""
Selenium tests for Browse Users page.
Run with: python -m pytest tests/test_browse_users.py -v
Requires Flask running on http://127.0.0.1:5000
"""
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = 'http://127.0.0.1:5000'


class BrowseUsersTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(3)

        # Sign up and log in once for all tests
        cls.driver.get(f'{BASE_URL}/logout')
        time.sleep(1)
        cls.driver.delete_all_cookies()

        timestamp = str(int(time.time()))
        cls.test_email = f'browse_{timestamp}@student.uwa.edu.au'

        # Signup
        cls.driver.get(f'{BASE_URL}/signup')
        time.sleep(1)
        cls.driver.find_element(By.NAME, 'name').send_keys('Browse Tester')
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

    def test_browse_page_opens(self):
        """Browse users page should load successfully after login."""
        self.driver.get(f'{BASE_URL}/browse')
        time.sleep(1)
        self.assertIn('browse', self.driver.current_url.lower())
        self.assertNotIn('login', self.driver.current_url.lower())

    def test_browse_page_has_search(self):
        """Browse page should contain a search/filter input."""
        self.driver.get(f'{BASE_URL}/browse')
        time.sleep(1)
        # Look for any input field (search box)
        inputs = self.driver.find_elements(By.TAG_NAME, 'input')
        selects = self.driver.find_elements(By.TAG_NAME, 'select')
        self.assertTrue(
            len(inputs) > 0 or len(selects) > 0,
            'Browse page should have search or filter inputs'
        )

    def test_search_box_accepts_input(self):
        """Search box should accept text input."""
        self.driver.get(f'{BASE_URL}/browse')
        time.sleep(1)
        inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
        if len(inputs) > 0:
            inputs[0].clear()
            inputs[0].send_keys('CITS3403')
            self.assertEqual(inputs[0].get_attribute('value'), 'CITS3403')
        else:
            # If no text input, check for select dropdown
            selects = self.driver.find_elements(By.TAG_NAME, 'select')
            self.assertTrue(len(selects) > 0, 'Should have search input or filter dropdown')


if __name__ == '__main__':
    unittest.main()
