from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("http://127.0.0.1:5000")
time.sleep(2)

links = driver.find_elements(By.TAG_NAME, "a")

link_texts = [link.text.lower() for link in links]

print(link_texts)

assert len(link_texts) > 0

print("Navbar links test passed")

driver.quit()