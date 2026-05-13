from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open signup page
driver.get("http://127.0.0.1:5000/signup")

time.sleep(2)

# Fill signup form
name = driver.find_element(By.NAME, "name")
name.send_keys("Fatima")

email = driver.find_element(By.NAME, "email")
email.send_keys("fatima@gmail.com")

password = driver.find_element(By.NAME, "password")
password.send_keys("123456")

time.sleep(2)

print("Signup form test passed")

driver.quit()