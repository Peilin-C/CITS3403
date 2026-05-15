import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = 'http://127.0.0.1:5000'

class SignupFormTests(unittest.TestCase):

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

    def test_signup_page_loads(self):
        self.driver.get(f'{BASE_URL}/signup')
        time.sleep(1)
        body = self.driver.find_element(By.TAG_NAME, 'body').text.lower()
        self.assertTrue('sign up' in body or 'create' in body)

    def test_signup_form_has_required_fields(self):
        self.driver.get(f'{BASE_URL}/signup')
        time.sleep(1)
        self.assertIsNotNone(self.driver.find_element(By.NAME, 'name'))
        self.assertIsNotNone(self.driver.find_element(By.NAME, 'email'))
        self.assertIsNotNone(self.driver.find_element(By.NAME, 'password'))
        self.assertIsNotNone(self.driver.find_element(By.NAME, 'confirm'))

    def test_signup_form_accepts_input(self):
        self.driver.get(f'{BASE_URL}/signup')
        time.sleep(1)
        self.driver.find_element(By.NAME, 'name').send_keys('Test User')
        self.driver.find_element(By.NAME, 'email').send_keys('newtest@uwa.edu.au')
        self.driver.find_element(By.NAME, 'password').send_keys('Password123')
        self.driver.find_element(By.NAME, 'confirm').send_keys('Password123')
        self.assertEqual(
            self.driver.find_element(By.NAME, 'email').get_attribute('value'),
            'newtest@uwa.edu.au'
        )

    def test_successful_signup_redirects(self):
        self.driver.get(f'{BASE_URL}/signup')
        time.sleep(1)
        timestamp = str(int(time.time()))
        self.driver.find_element(By.NAME, 'name').send_keys('New User')
        self.driver.find_element(By.NAME, 'email').send_keys(f'new_{timestamp}@uwa.edu.au')
        self.driver.find_element(By.NAME, 'password').send_keys('Password123')
        self.driver.find_element(By.NAME, 'confirm').send_keys('Password123')
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(3)
        self.assertNotIn('signup', self.driver.current_url.lower())

if __name__ == '__main__':
    unittest.main()
