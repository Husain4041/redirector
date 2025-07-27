from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
import time
import json
import os

def scrape_model_slugs(make_slug):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(f"https://www.dubizzle.com/motors/used-cars/")
    time.sleep(5)  # Wait for the page to load

    model_slugs = set()  # To store unique model slugs
    filepath = 'car_data/make_model_links.json'
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            full_data = json.load(f)
    else:
        full_data = {"dubizzle": {}}
    # full_data = {"dubizzle": {make_slug: {}}}

    if "dubizzle" not in full_data:
        full_data["dubizzle"] - {}

    if make_slug not in full_data["dubizzle"]:
        full_data["dubizzle"][make_slug] = {}

    input_box = driver.find_element(By.XPATH, '//input[@placeholder="Search Make, Model"]')
    input_box.click()
    input_box.clear()
    time.sleep(3)
    input_box.send_keys(make_slug + ' ')
    time.sleep(5)

    model_dropdown = driver.find_element(By.CSS_SELECTOR, 'ul[aria-labelledby="vehicle-autocomplete-label"]')
    options = model_dropdown.find_elements(By.CSS_SELECTOR, 'div[data-option-index]')
    no_of_models = len(options)
    print(f"Found {no_of_models} options for make: {make_slug}")
    # input_box.clear()

    for index in range(len(options)):
        try:
            # Re-open dropdown each time (since navigating resests it)
            input_box = driver.find_element(By.XPATH, '//input[@placeholder="Search Make, Model"]')
            input_box.click()
            input_box.clear()
            time.sleep(3)
            input_box.send_keys(make_slug + ' ')
            time.sleep(5)

            # Re-fetch the options after reopening the dropdown
            model_dropdown = driver.find_element(By.CSS_SELECTOR, 'ul[aria-labelledby="vehicle-autocomplete-label"]')
            options = model_dropdown.find_elements(By.CSS_SELECTOR, 'div[data-option-index]')

            # if index > 0 and (index) / 10 == 1:
            #     driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;", model_dropdown)
            #     time.sleep(2)  # Wait for the scroll to complete

            scroll_count = index // 10
            for _ in range(scroll_count):
                driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;",
                    model_dropdown
                )
                time.sleep(1)


            option = options[index] # Get the specific option by index
            model_name = option.text.strip()

            if not model_name:
                continue
                
            option.click()  # Click the option to select it
            time.sleep(3)  # Wait for the model to be selected

            href = driver.current_url
            print(f"{model_name} URL: {href}")
            model_slugs.add(href)
            full_data['dubizzle'][make_slug][model_name] = href

            driver.back()
            time.sleep(3)  # Wait for the page to load after going back
        except Exception as e:
            print(f"Error processing option {index} for {make_slug}: {e}")
            
        

    driver.quit()
    

    # anchors = driver.find_elements(By.TAG_NAME, 'a')  # Find all anchor tags
    # for a in anchors: 
    #     href = a.get_attribute('href') # Get the href attribute
        
    #     parsed = urlparse(href) # Parses the URL into usable components
    #     path_parts = parsed.path.strip("/").split('/') # Strip path of leading/trailing slashes then split by slashes


    every_model_links = list(model_slugs)  # Sort the model slugs alphabetically
    with open(filepath, 'w') as f:
        json.dump(full_data, f, indent=2)

    return len(full_data["dubizzle"][make_slug])

if __name__ == "__main__":
    with open('car_data/car_makes.json', 'r') as f:
        car_makes = json.load(f)

    # for make in car_makes:
    #     print(f"Scraped {scrape_model_slugs(make)} links for {make}.")

    print(f"Scraped {scrape_model_slugs('abarth')} links for abarth.")
    print(f"Scraped {scrape_model_slugs('acura')} links for acura.")