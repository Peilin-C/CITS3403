from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Homepage test
driver.get("http://127.0.0.1:5000")
time.sleep(2)

assert "Study" in driver.page_source
print("Homepage test passed")


# Login page test
driver.get("http://127.0.0.1:5000/login")
time.sleep(2)

assert "login" in driver.page_source.lower()
print("Login page test passed")


# Signup page test
driver.get("http://127.0.0.1:5000/signup")
time.sleep(2)

assert "signup" in driver.page_source.lower() or "sign up" in driver.page_source.lower()
print("Signup page test passed")


# Browse page test
driver.get("http://127.0.0.1:5000/browse")
time.sleep(2)

print("Browse page test passed")


driver.quit()

print("All navigation tests passed")