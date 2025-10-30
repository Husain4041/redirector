from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests
from PIL import Image
import io
from pathlib import Path

def save_images(urls_list, num_images, make):
    downloaded_count = 0

    train_dir = Path("/data/cars_copy/train/")
    test_dir = Path("/data/cars_copy/test/")

    if not train_dir.exists():
        print("doesnt exist bro")

    for idx, url in enumerate(urls_list):
        try:
            img_response = requests.get(url)
            img_response.raise_for_status()

            img = Image.open(io.BytesIO(img_response.content))
            img = img.convert("RGB")

            if downloaded_count < num_images * 0.8:
                save_path = train_dir / make / f"{make}_{downloaded_count + 1}.jpg"
            else:
                save_path = test_dir / make / f"{make}_{downloaded_count + 1}.jpg"

            img.save(save_path, "JPEG", quality=85)
            downloaded_count += 1
            print(f" Downloaded: {save_path.name}")

        except Exception as e:
            print(f"Failed to download image from {url}: {e}")
            continue


def scrape_dubizzle_images(make):

    urls_list = []

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(f"https://www.dubizzle.com/motors/used-cars/{make}/")
    time.sleep(5) 

    listings_container = driver.find_element(By.CSS_SELECTOR, 'div[id="listings-container"]')
    listing_card_wrapper = listings_container.find_element(By.CSS_SELECTOR, 'div[id="listing-card-wrapper"]')
    listings = listing_card_wrapper.find_elements(By.CSS_SELECTOR, 'a[data-testid]')
    no_of_listings = len(listings)
    print(f'Number of listings found for {make} on page 1: {no_of_listings}')

    for i in range(no_of_listings):
        try:
            listings_container = driver.find_element(By.CSS_SELECTOR, 'div[id="listings-container"]')
            listing_card_wrapper = listings_container.find_element(By.CSS_SELECTOR, 'div[id="listing-card-wrapper"]')
            listings = listing_card_wrapper.find_elements(By.CSS_SELECTOR, 'a[data-testid]')

            # Click on each listing
            listings[i].click()
            time.sleep(3)
            print(f"Successfully opened listing {i+1} for {make}")

            # Click on image to open gallery
            headline_image = driver.find_element(By.CSS_SELECTOR, 'div[data-testid]')
            headline_image.click()
            time.sleep(3)

            # Save images
            try:
                img = driver.find_elements(By.CSS_SELECTOR, 'ul[class="MuiImageList-root MuiImageList-standard mui-style-1kt5npx"] li img')
                no_of_images = len(img)
                print(f'Number of images found for listing {i+1} for {make}: {no_of_images}')
                for j in range(no_of_images):
                    img_url = img[j].get_attribute('src')
                    print(f"Image URL {j+1} for {make}: {img_url}")
                    urls_list.append(img_url)

            except Exception as e:
                print(f"Error while accessing image gallery for listing {i+1} for {make}: {e}")


            # Go back to gallery view
            driver.back()
            time.sleep(3)

            # Go back to the listings page
            driver.back()
            time.sleep(3)

        except Exception as e:
            print(f"Error processing listing {i+1} for {make}: {e}")

    print(f'Total images collected for {make}: {len(urls_list)}')
    # Save images after collecting from each listing
    save_images(urls_list, 100, make)



    driver.quit()

makes = ['audi', 'bmw', 'ford', 'mercedes', 'toyota']
print("Current working directory:", os.getcwd())
# for make in makes:
scrape_dubizzle_images("audi")
