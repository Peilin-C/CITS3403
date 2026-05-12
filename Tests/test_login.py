from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Open Chrome browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open your Flask website
driver.get("http://127.0.0.1:5000")

# Wait 3 seconds so you can see it
time.sleep(3)

print("Website opened successfully")

# Close browser
driver.quit()