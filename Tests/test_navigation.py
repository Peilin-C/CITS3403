import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = 'http://127.0.0.1:5000'

class NavigationTests(unittest.TestCase):

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

    def test_login_page_loads(self):
        self.driver.get(f'{BASE_URL}/login')
        time.sleep(2)
        self.assertIn('login', self.driver.page_source.lower())

    def test_signup_page_loads(self):
        self.driver.get(f'{BASE_URL}/signup')
        time.sleep(2)
        body = self.driver.page_source.lower()
        self.assertTrue('sign up' in body or 'signup' in body or 'create' in body)

    def test_browse_redirects_to_login_when_not_logged_in(self):
        self.driver.get(f'{BASE_URL}/browse')
        time.sleep(2)
        self.assertIn('login', self.driver.current_url.lower())

if __name__ == '__main__':
    unittest.main()
