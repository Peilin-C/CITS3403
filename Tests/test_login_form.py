from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open login page
driver.get("http://127.0.0.1:5000/login")

time.sleep(2)

# Find email field
email = driver.find_element(By.NAME, "email")
email.send_keys("test@gmail.com")

# Find password field
password = driver.find_element(By.NAME, "password")
password.send_keys("123456")

time.sleep(2)

print("Login form input test passed")

driver.quit()