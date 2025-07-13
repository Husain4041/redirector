from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def scrape_makes_models():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.dubicars.com/new-cars")
    time.sleep(5)  # Wait for the page to load

    all_makes = set() # To store unique makes

    # Find the input box and enter the letter
    input_box = driver.find_element(By.XPATH, '//span[contains(@placeholder, "Select make")]')
    # input_box.clear()
    input_box.click()
    time.sleep(2) # Wait for dropdown to appear   

    dropdown = driver.find_element(By.XPATH, '//div[@class="dropdown-options"]')
    options = dropdown.find_elements(By.CSS_SELECTOR, 'li[data-url]')

    for option in options:
        make = option.text.strip()
        all_makes.add(make.lower())

    sorted_makes = sorted(list(all_makes))  # Sort the makes alphabetically
    with open('dubizzle_makes.json', 'w') as f:
        json.dump(sorted_makes, f, indent=2)

    print(f"Scraped {len(sorted_makes)} unique makes. Saved to 'dubizzle_makes.json'.")

if __name__ == "__main__":
    scrape_makes_models()
