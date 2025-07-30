import json
import os
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor, as_completed

# Lock for safely writing to shared JSON
data_lock = threading.Lock()

# Shared path to save data
json_path = 'car_data/multi_threading_links.json'

def scrape_model_slugs(make_slug):
    local_data = {}

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        driver.get("https://www.dubizzle.com/motors/used-cars/")
        time.sleep(4)

        # Search for the make in the input box
        def open_model_dropdown():
            input_box = driver.find_element(By.XPATH, '//input[@placeholder="Search Make, Model"]')
            input_box.click()
            time.sleep(2.5)
            input_box.clear()
            time.sleep(2.5)
            input_box.send_keys(make_slug + ' ')
            time.sleep(6)
            return input_box

        input_box = open_model_dropdown()

        # Initial fetch of model options
        model_dropdown = driver.find_element(By.CSS_SELECTOR, 'ul[aria-labelledby="vehicle-autocomplete-label"]')
        model_elements = model_dropdown.find_elements(By.CSS_SELECTOR, 'div[data-option-index]')
        model_count = len(model_elements)
        print(f"[{make_slug}] Found {model_count} models.")

        for index in range(model_count):
            try:
                # Re-open dropdown and re-fetch model list
                input_box = open_model_dropdown()
                model_dropdown = driver.find_element(By.CSS_SELECTOR, 'ul[aria-labelledby="vehicle-autocomplete-label"]')
                model_elements = model_dropdown.find_elements(By.CSS_SELECTOR, 'div[data-option-index]')

                # Scroll as needed (index-based chunking)
                scroll_count = index // 10
                for _ in range(scroll_count):
                    driver.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;",
                        model_dropdown
                    )
                    time.sleep(1)

                option = model_elements[index]
                model_name = option.text.strip()

                if not model_name:
                    continue

                option.click()
                time.sleep(4)

                href = driver.current_url
                local_data[model_name] = href
                print(f"[{make_slug}] {model_name} → {href}")

                driver.back()
                time.sleep(3)

            except Exception as e:
                print(f"[{make_slug}] Failed to get model at index {index}: {e}")

    except Exception as e:
        print(f"[{make_slug}] ERROR: {e}")
    finally:
        driver.quit()

    # Safely update JSON
    with data_lock:
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                full_data = json.load(f)
        else:
            full_data = {"dubizzle": {}}

        if make_slug not in full_data["dubizzle"]:
            full_data["dubizzle"][make_slug] = {}

        full_data["dubizzle"][make_slug].update(local_data)

        with open(json_path, 'w') as f:
            json.dump(full_data, f, indent=2)

    return len(local_data)


def run_scraper_with_threads(car_makes, thread_count=2):
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = {executor.submit(scrape_model_slugs, make): make for make in car_makes}

        try:
            for future in as_completed(futures):
                make = futures[future]
                try:
                    count = future.result()
                    print(f"[{make}] ✅ Scraped {count} model links.")
                except Exception as e:
                    print(f"[{make}] ❌ Failed with error: {e}")
        except KeyboardInterrupt:
            print("\n🚨 Interrupted by user. Shutting down threads...")
            executor.shutdown(wait=False, cancel_futures=True)
            raise


if __name__ == "__main__":
    try:
        with open('car_data/car_makes.json', 'r') as f:
            car_makes = json.load(f)

        thread_count = 5  # Safe default, raise to 4+ if confident in your machine's capacity
        run_scraper_with_threads(car_makes, thread_count)

    except KeyboardInterrupt:
        print("\n❌ Program interrupted manually.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


# --- Worked better, scraped model count and 1 link then break --- #
# import json
# import os
# import time
# import threading
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from concurrent.futures import ThreadPoolExecutor, as_completed

# # Lock for safely writing to shared JSON
# data_lock = threading.Lock()

# # Shared path to save data
# json_path = 'car_data/multi_threading_links.json'

# def scrape_model_slugs(make_slug):
#     local_data = {}

#     # Initialize browser
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     try:
#         driver.get("https://www.dubizzle.com/motors/used-cars/")
#         time.sleep(4)

#         input_box = driver.find_element(By.XPATH, '//input[@placeholder="Search Make, Model"]')
#         input_box.click()
#         input_box.clear()
#         time.sleep(5)
#         input_box.send_keys(make_slug + ' ')
#         time.sleep(5)

#         model_dropdown = driver.find_element(By.CSS_SELECTOR, 'ul[aria-labelledby="vehicle-autocomplete-label"]')
#         options = model_dropdown.find_elements(By.CSS_SELECTOR, 'div[data-option-index]')
#         print(f"[{make_slug}] Found {len(options)} models.")

#         for index, option in enumerate(options):
#             # Scroll as needed
#             scroll_count = index // 10
#             for _ in range(scroll_count):
#                 driver.execute_script(
#                     "arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;",
#                     model_dropdown
#                 )
#                 time.sleep(1)

#             model_name = option.text.strip()
#             if not model_name:
#                 continue

#             option.click()
#             time.sleep(4)

#             url = driver.current_url
#             local_data[model_name] = url
#             print(f"[{make_slug}] {model_name} → {url}")

#             driver.back()
#             time.sleep(3)

#             # Re-open the input for next round
#             input_box = driver.find_element(By.XPATH, '//input[@placeholder="Search Make, Model"]')
#             input_box.click()
#             input_box.clear()
#             time.sleep(5)
#             input_box.send_keys(make_slug + ' ')
#             time.sleep(6)
#             model_dropdown = driver.find_element(By.CSS_SELECTOR, 'ul[aria-labelledby="vehicle-autocomplete-label"]')
#             options = model_dropdown.find_elements(By.CSS_SELECTOR, 'div[data-option-index]')

#     except Exception as e:
#         print(f"[{make_slug}] ERROR: {e}")
#     finally:
#         driver.quit()

#     # Write data safely to shared file
#     with data_lock:
#         if os.path.exists(json_path):
#             with open(json_path, 'r') as f:
#                 full_data = json.load(f)
#         else:
#             full_data = {"dubizzle": {}}

#         if make_slug not in full_data["dubizzle"]:
#             full_data["dubizzle"][make_slug] = {}

#         full_data["dubizzle"][make_slug].update(local_data)

#         with open(json_path, 'w') as f:
#             json.dump(full_data, f, indent=2)

#     return len(local_data)


# def run_scraper_with_threads(car_makes, thread_count=4):
#     with ThreadPoolExecutor(max_workers=thread_count) as executor:
#         futures = {executor.submit(scrape_model_slugs, make): make for make in car_makes}

#         try:
#             for future in as_completed(futures):
#                 make = futures[future]
#                 try:
#                     count = future.result()
#                     print(f"[{make}] ✅ Scraped {count} model links.")
#                 except Exception as e:
#                     print(f"[{make}] ❌ Failed with error: {e}")
#         except KeyboardInterrupt:
#             print("\n🚨 Interrupted by user. Shutting down threads...")
#             executor.shutdown(wait=False, cancel_futures=True)
#             raise


# if __name__ == "__main__":
#     try:
#         with open('car_data/car_makes.json', 'r') as f:
#             car_makes = json.load(f)

#         thread_count = 2  # You can increase this for faster scraping
#         run_scraper_with_threads(car_makes, thread_count)

#     except KeyboardInterrupt:
#         print("\n❌ Program interrupted manually.")
#     except Exception as e:
#         print(f"\n❌ Unexpected error: {e}")


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from concurrent.futures import ThreadPoolExecutor, as_completed
# import time
# import json
# import os
# import threading

# # Thread-safe data structure
# data_lock = threading.Lock()
# full_data = {"dubizzle": {}}

# def scrape_model_slugs(make_slug):
#     global full_data
#     filepath = 'car_data/multi_threading_scraper_links.json'

#     with data_lock:
#         if make_slug in full_data["dubizzle"]:
#             print(f'{make_slug} already exists in data. Skipping.')
#             return 0

#     # Setup new driver per thread
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     driver.get("https://www.dubizzle.com/motors/used-cars/")
#     time.sleep(3)

#     # Open dropdown and search for make
#     input_box = driver.find_element(By.XPATH, '//input[@placeholder="Search Make, Model"]')
#     input_box.click()
#     input_box.clear()
#     input_box.send_keys(make_slug + ' ')
#     time.sleep(5)

#     model_dropdown = driver.find_element(By.CSS_SELECTOR, 'ul[aria-labelledby="vehicle-autocomplete-label"]')
#     options = model_dropdown.find_elements(By.CSS_SELECTOR, 'div[data-option-index]')
#     no_of_models = len(options)

#     print(f"[{make_slug}] Found {no_of_models} models.")

#     local_data = {}

#     for index in range(no_of_models):
#         try:
#             input_box = driver.find_element(By.XPATH, '//input[@placeholder="Search Make, Model"]')
#             input_box.click()
#             input_box.clear()
#             time.sleep(3)
#             input_box.send_keys(make_slug + ' ')
#             time.sleep(5)

#             model_dropdown = driver.find_element(By.CSS_SELECTOR, 'ul[aria-labelledby="vehicle-autocomplete-label"]')
#             options = model_dropdown.find_elements(By.CSS_SELECTOR, 'div[data-option-index]')

#             scroll_count = index // 10
#             for _ in range(scroll_count):
#                 driver.execute_script(
#                     "arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;",
#                     model_dropdown
#                 )
#                 time.sleep(1)

#             option = options[index]
#             model_name = option.text.strip()
#             if not model_name:
#                 continue

#             option.click()
#             time.sleep(3)

#             href = driver.current_url
#             local_data[model_name] = href

#             driver.back()
#             time.sleep(3)

#         except Exception as e:
#             print(f"[{make_slug}] Error at index {index}: {e}")
#             continue
#         except KeyboardInterrupt:
#             print("Interrupted! Exiting gracefully...")
#             driver.quit()
#             exit()

#     driver.quit()

#     with data_lock:
#         full_data["dubizzle"][make_slug] = local_data

#     return len(local_data)

# def run_scraper(thread_count):
#     global full_data
#     filepath = 'car_data/multi_threading_scraper_links.json'

#     # Load existing data if present
#     if os.path.exists(filepath):
#         with open(filepath, 'r') as f:
#             full_data = json.load(f)
#     else:
#         full_data = {"dubizzle": {}}

#     # Load all makes
#     with open('car_data/car_makes.json', 'r') as f:
#         car_makes = json.load(f)

#     with ThreadPoolExecutor(max_workers=thread_count) as executor:
#         futures = {executor.submit(scrape_model_slugs, make): make for make in car_makes}
#         for future in as_completed(futures):
#             make = futures[future]
#             try:
#                 count = future.result()
#                 print(f"[{make}] Completed scraping {count} model links.")
#             except Exception as e:
#                 print(f"[{make}] Failed with error: {e}")

#     # Save full data after all threads are done
#     with open(filepath, 'w') as f:
#         json.dump(full_data, f, indent=2)

# if __name__ == "__main__":
#     # Change the number to test different thread counts
#     run_scraper(thread_count=2)
