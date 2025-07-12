from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def scrape_makes_models():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://dubai.dubizzle.com/motors/used-cars/")
    time.sleep(5)  # Wait for the page to load

    categories = driver.find_elements(By.CSS_SELECTOR, )