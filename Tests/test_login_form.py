import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = 'http://127.0.0.1:5000'

class LoginFormTests(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(5)

    def tearDown(self):
        self.driver.quit()

    def test_login_form_accepts_email(self):
        self.driver.get(f'{BASE_URL}/login')
        time.sleep(1)
        email_field = self.driver.find_element(By.NAME, 'email')
        email_field.send_keys('test@uwa.edu.au')
        self.assertEqual(email_field.get_attribute('value'), 'test@uwa.edu.au')

    def test_login_form_accepts_password(self):
        self.driver.get(f'{BASE_URL}/login')
        time.sleep(1)
        password_field = self.driver.find_element(By.NAME, 'password')
        password_field.send_keys('Password123')
        self.assertEqual(password_field.get_attribute('value'), 'Password123')

    def test_login_form_has_submit_button(self):
        self.driver.get(f'{BASE_URL}/login')
        time.sleep(1)
        submit = self.driver.find_elements(By.CSS_SELECTOR, 'button[type="submit"]')
        self.assertTrue(len(submit) > 0, 'Login form should have submit button')

if __name__ == '__main__':
    unittest.main()
