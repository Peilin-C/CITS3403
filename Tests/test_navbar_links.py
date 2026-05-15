import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = 'http://127.0.0.1:5000'

class NavbarLinksTests(unittest.TestCase):

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

    def test_navbar_has_links(self):
        self.driver.get(BASE_URL)
        time.sleep(2)
        links = self.driver.find_elements(By.TAG_NAME, 'a')
        self.assertTrue(len(links) > 0, 'Navbar should have links')

    def test_navbar_has_home_link(self):
        self.driver.get(BASE_URL)
        time.sleep(2)
        body = self.driver.page_source.lower()
        self.assertIn('home', body)

    def test_navbar_has_browse_link(self):
        self.driver.get(BASE_URL)
        time.sleep(2)
        body = self.driver.page_source.lower()
        self.assertIn('browse', body)

    def test_navbar_has_sessions_link(self):
        self.driver.get(BASE_URL)
        time.sleep(2)
        body = self.driver.page_source.lower()
        self.assertIn('sessions', body)

if __name__ == '__main__':
    unittest.main()
