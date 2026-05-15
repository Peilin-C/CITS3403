import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = 'http://127.0.0.1:5000'

class LoginButtonTests(unittest.TestCase):

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

    def test_login_button_exists_on_homepage(self):
        self.driver.get(BASE_URL)
        time.sleep(2)
        login_links = self.driver.find_elements(By.LINK_TEXT, 'Log In')
        self.assertTrue(len(login_links) > 0, 'Login button should exist on homepage')

    def test_login_button_navigates_to_login_page(self):
        self.driver.get(BASE_URL)
        time.sleep(2)
        login_link = self.driver.find_element(By.LINK_TEXT, 'Log In')
        login_link.click()
        time.sleep(2)
        self.assertIn('login', self.driver.current_url.lower())

    def test_signup_button_exists_on_homepage(self):
        self.driver.get(BASE_URL)
        time.sleep(2)
        signup_links = self.driver.find_elements(By.LINK_TEXT, 'Sign Up')
        self.assertTrue(len(signup_links) > 0, 'Sign Up button should exist on homepage')

if __name__ == '__main__':
    unittest.main()
