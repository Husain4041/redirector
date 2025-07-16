from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def scrape_makes():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.dubicars.com/new-cars")
    time.sleep(5)  # Wait for the page to load

    all_makes = set() # To store unique makes
    all_makes_data_url = set() # To store unique makes with data-url
    makes_dict = {}

    # Find the input box and enter the letter
    input_box = driver.find_element(By.XPATH, '//span[contains(@placeholder, "Select make")]')
    # input_box.clear()
    input_box.click()
    time.sleep(2) # Wait for dropdown to appear   

    dropdown = driver.find_element(By.XPATH, '//div[@class="dropdown-options"]')
    options = dropdown.find_elements(By.CSS_SELECTOR, 'li[data-url]')

    for option in options:
        make = option.text.strip()
        data_url = option.get_attribute('data-url')
        all_makes.add(make.lower())
        all_makes_data_url.add(data_url)
        makes_dict[make.lower()] = data_url

    sorted_makes = sorted(list(all_makes))  # Sort the makes alphabetically
    with open('car_makes_with_data_url.json', 'w') as f:
        json.dump(makes_dict, f, indent=2)

    print(f"Scraped {len(sorted_makes)} unique makes. Saved to 'car_makes_with_data_url.json'.")

def scrape_models(make, data_url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.dubicars.com/new-cars")
    time.sleep(3)  # Wait for the page to load

    models_for_this_make = set()  # To store unique models for the given make

    # Click on make input box to make the other input box appear
    make_input = driver.find_element(By.XPATH, '//span[contains(@placeholder, "Select make")]')
    make_input.click()
    input_box = driver.find_element(By.XPATH, '//input[@placeholder="Search Make"]')
    time.sleep(2)  # Wait for dropdown to appear
    input_box.send_keys(make)
    this_make = driver.find_element(By.CSS_SELECTOR, f'li[data-url="{data_url}"]')
    this_make.click()
    time.sleep(2)

    model_dropdown = driver.find_element(By.XPATH, '//div[@field-label="Select model"]')
    options = model_dropdown.find_elements(By.CSS_SELECTOR, 'li[data-url]')

    for option in options:
        model = option.text.strip()
        models_for_this_make.add(model.lower())
    
    driver.quit()  # Close the browser after scraping
    
    return sorted(list(models_for_this_make))


if __name__ == "__main__":
    # scrape_makes()
    with open('car_makes_with_data_url.json', 'r') as f:
        all_makes = json.load(f)

    # Print all makes with their data_url s
    # for make in all_makes:
    #     print(f"{make}: {all_makes[make]}")

    all_makes_models = {} # Dictionary to hold makes and their models
    
    for make in all_makes:
        print(f'Scraping models for make: {make}')
        all_makes_models[make] = scrape_models(make, all_makes[make])
        print(f'Found {len(all_makes_models[make])} models for make: {make}')

    with open('car_makes_models.json', 'w') as f:
        json.dump(all_makes_models, f, indent=2)

    # Example usage for a specific make
    # all_makes_models["audi"] = scrape_models("audi", all_makes["audi"])
    # for model in all_makes_models["audi"]:
    #     print(f'These are the {len(all_makes_models["audi"])} models found for audi: {model}')