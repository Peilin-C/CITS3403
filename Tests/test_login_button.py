from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open homepage
driver.get("http://127.0.0.1:5000")

time.sleep(2)

# Find login link/button
login_button = driver.find_element(By.LINK_TEXT, "Log In")

# Click it
login_button.click()

time.sleep(2)

# Check if login page opened
assert "login" in driver.page_source.lower()

print("Login button navigation test passed")

driver.quit()