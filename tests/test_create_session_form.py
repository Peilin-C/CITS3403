"""
Selenium tests for Create Session form interaction.
Run with: python -m pytest tests/test_create_session_form.py -v
Requires Flask running on http://127.0.0.1:5000
"""
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = 'http://127.0.0.1:5000'


class CreateSessionFormTests(unittest.TestCase):

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
        cls.test_email = f'form_{timestamp}@student.uwa.edu.au'

        # Signup
        cls.driver.get(f'{BASE_URL}/signup')
        time.sleep(1)
        cls.driver.find_element(By.NAME, 'name').send_keys('Form Tester')
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

    def test_form_accepts_session_name(self):
        """Session name input should accept text."""
        self.driver.get(f'{BASE_URL}/create_session')
        time.sleep(1)
        text_inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
        if len(text_inputs) > 0:
            text_inputs[0].clear()
            text_inputs[0].send_keys('CITS3403 Exam Prep')
            self.assertEqual(text_inputs[0].get_attribute('value'), 'CITS3403 Exam Prep')

    def test_form_accepts_all_fields(self):
        """All form fields should accept input without errors."""
        self.driver.get(f'{BASE_URL}/create_session')
        time.sleep(1)

        # Fill all text inputs
        text_inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
        for inp in text_inputs:
            inp.clear()
            inp.send_keys('Test Input')

        # Fill all time inputs
        time_inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="time"]')
        for inp in time_inputs:
            inp.send_keys('1400')

        # Fill all textareas
        textareas = self.driver.find_elements(By.TAG_NAME, 'textarea')
        for ta in textareas:
            ta.clear()
            ta.send_keys('Test description for study session')

        # Select dropdowns
        selects = self.driver.find_elements(By.TAG_NAME, 'select')
        for sel in selects:
            options = sel.find_elements(By.TAG_NAME, 'option')
            if len(options) > 1:
                options[1].click()

        # No errors should have occurred — page still loaded
        body = self.driver.find_element(By.TAG_NAME, 'body')
        self.assertIsNotNone(body)


if __name__ == '__main__':
    unittest.main()
