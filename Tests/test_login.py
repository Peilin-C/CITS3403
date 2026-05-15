import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = 'http://127.0.0.1:5000'

class LoginTests(unittest.TestCase):

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

    def test_homepage_loads(self):
        self.driver.get(BASE_URL)
        time.sleep(2)
        self.assertIn('Study', self.driver.page_source)
        self.assertEqual(self.driver.current_url, f'{BASE_URL}/')

    def test_login_page_loads(self):
        self.driver.get(f'{BASE_URL}/login')
        time.sleep(1)
        self.assertIn('login', self.driver.current_url.lower())
        body = self.driver.find_element(By.TAG_NAME, 'body').text.lower()
        self.assertTrue('email' in body or 'log in' in body.lower())

    def test_login_form_has_fields(self):
        self.driver.get(f'{BASE_URL}/login')
        time.sleep(1)
        email_field = self.driver.find_element(By.NAME, 'email')
        password_field = self.driver.find_element(By.NAME, 'password')
        self.assertIsNotNone(email_field)
        self.assertIsNotNone(password_field)

    def test_login_with_wrong_credentials_shows_error(self):
        self.driver.get(f'{BASE_URL}/login')
        time.sleep(1)
        self.driver.find_element(By.NAME, 'email').send_keys('wrong@uwa.edu.au')
        self.driver.find_element(By.NAME, 'password').send_keys('wrongpassword')
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(2)
        self.assertIn('login', self.driver.current_url.lower())

if __name__ == '__main__':
    unittest.main()
