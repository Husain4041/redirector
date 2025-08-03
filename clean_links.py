from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import json
import re

# ----- Helper Function ----- #
def contains_special_char(s):
    for char in s:
        if not char.isalnum():
            return True, char
    return False, ' '

def flag_make(make, og_count):
    with open('car_data/multi_threading_links.json', 'r') as f:
        full_data = json.load(f)

    count = 0
    flagged = False
    for _ in full_data["dubizzle"][make]:
        count+=1

    if (count != og_count):
        flagged = True
        print(f"[{make}]: There are {count} model links scraped.\n There should be {og_count}.")
    
    return flagged
# ------ END OF HELPER ------ #

def find_missing_models(make, model_dict):

    og_set = set()
    incomplete_set = set()

    filepath = 'car_data/multi_threading_links_completed.json'
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            incomplete_data = json.load(f)
    else:
        incomplete_data = {"dubizzle": {}}

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.dubizzle.com/motors/used-cars/")
    time.sleep(4)

    def open_dropdown():
        input_box = driver.find_element(By.XPATH, '//input[@placeholder="Search Make, Model"]')
        input_box.click()
        input_box.clear()
        time.sleep(2.5)
        input_box.send_keys(make + " ")
        time.sleep(4)
        return input_box

    try:
        input_box = open_dropdown()
        model_dropdown = driver.find_element(By.CSS_SELECTOR, 'ul[aria-labelledby="vehicle-autocomplete-label"]')

        seen_models = set()
        last_seen_count = -1
        attempts = 0

        while attempts < 2:
            options = model_dropdown.find_elements(By.CSS_SELECTOR, 'div[data-option-index]')
            for option in options:
                text = option.text.strip()
                if text:
                    seen_models.add(text)

            if len(seen_models) == last_seen_count:
                attempts += 1
            else:
                attempts = 0
                last_seen_count = len(seen_models)

            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;",
                model_dropdown
            )
            time.sleep(1.2)

        og_set = seen_models
        print("------------------------------------------------------------\n")
        print(f"--->Found {len(og_set)} unique model options for make: \n{make}\n")
        print("------------------------------------------------------------\n")
        print(f"--->This is the original set of {len(og_set)} models: \n{og_set}\n")

        for model in model_dict:
            incomplete_set.add(model)
        print("------------------------------------------------------------\n")
        print(f"--->This is the incomplete set of {len(incomplete_set)} models: \n{incomplete_set}\n")

        missing_models = og_set.difference(incomplete_set)
        print("------------------------------------------------------------\n")
        print(f"--->These models are missing from [{make}]: {missing_models}\n")

        for model in missing_models:
            missing_link = find_missing_link(model)
            model_dict[model] = missing_link
            print("------------------------------------------------------------\n")
            print(f"[{make}]: [{model}] -> {missing_link}")

    except Exception as e:
        print(f"[{make}] Failed to find missing links: {e}")
    finally:
        driver.quit()

    return dict(sorted(model_dict.items()))

def find_missing_link(model):
    print("------------------------------------------------------------\n")
    print(f"--->Looking up {model}\n")
    print("------------------------------------------------------------\n")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.dubizzle.com/motors/used-cars/")
    time.sleep(4)

    input_box = driver.find_element(By.XPATH, '//input[@placeholder="Search Make, Model"]')
    input_box.click()
    input_box.clear()
    time.sleep(2.5)
    input_box.send_keys(model)
    time.sleep(4)
    input_box.send_keys(Keys.ENTER)
    time.sleep(4)


    url = driver.current_url
    driver.quit()

    return url

def clean_models(make, model_dict):
    removed_models = []
    new_model_dict = {}
    for model in model_dict:
        # make_from_model = model.split(" ")
        make_from_model = re.findall(r"[\w']+", model)
        # print(f"This is the list of words in {model}: {make_from_model}")
        if (len(make.split(" ")) == 2 and len(make_from_model) >= 2):
            if (make.split(" ")[0] + make.split(" ")[1] == make_from_model[0].lower() or 
                make == make_from_model[0].lower() + " " + make_from_model[1].lower()):
                new_model_dict[model] = model_dict[model]
            else:
                removed_models.append(model)
        elif len(make.split(" ")) == 1:
            if (make == make_from_model[0].lower()):
                new_model_dict[model] = model_dict[model]
            else:
                removed_models.append(model)

    return new_model_dict, removed_models

if __name__ == "__main__":
    
    # with open('car_data/make_model_links.json', 'r') as f:
    #     full_data = json.load(f)

    with open('car_data/models_count.json', 'r') as f:
        count_data = json.load(f)

    with open('car_data/multi_threading_links.json', 'r') as f:
        incomplete_data = json.load(f)

    complete_data = {"dubizzle": {}}

    flagged_makes_count = 0
    for make in incomplete_data["dubizzle"]:
        if flag_make(make, count_data["dubizzle"][make]):
            flagged_makes_count+=1
            print("------------------------------------------------------------\n")
            print(f'--->[{make}] has been flagged as incomplete\n')
            print("------------------------------------------------------------\n")
            complete_dict = find_missing_models(make, model_dict=incomplete_data["dubizzle"][make])
            complete_data["dubizzle"][make] = complete_dict
            print("------------------------------------------------------------\n")
            print(f"--->This is the complete dictionary with {len(complete_dict)} models: \n{complete_dict.keys()}\n")
            print("------------------------------------------------------------\n")
        else:
            complete_data["dubizzle"][make] = incomplete_data["dubizzle"][make]

        with open('car_data/filled_multi_threading_links.json', 'w') as f:
            json.dump(complete_data, f, indent=2)

    # print(f"{flagged_makes_count} makes were flagged as having missing models")

    # true_model = False
    
    # for make in full_data["dubizzle"]:
    #     model_dict = full_data["dubizzle"][make]

    #     # ----- Printing the current make and models for that make ----- #
    #     # print(f"This is the make: {make} and these are the {len(model_dict)} current models: ")
    #     # for model in model_dict:
    #     #     print(model)
    #     # ------------------------- END OF PRINT FUNTCTION --------------#
        
    #     new_model_dict, removed_models_list = clean_models(make, model_dict)

    #     print(f"These models have been removed for infringement reasons: {removed_models_list}")
    #     # print(f"These are the {len(new_model_dict)} true models for {make}:")

    #     for models in new_model_dict:
    #         # print(models)
    #         new_model_dict[models] = model_dict[models]
    #     # print(new_model_dict)
    #     full_data["dubizzle"][make] = new_model_dict

    # with open('car_data/cleaned_model_links.json', 'w') as f:
    #     json.dump(full_data, f, indent=2)