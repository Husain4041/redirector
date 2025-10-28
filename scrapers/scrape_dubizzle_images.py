from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_dubizzle_images(make):
    
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

                    # img[j].click()
                    # time.sleep(1)
                    print(f"Image URL {j+1} for {make}: {img[j].get_attribute('src')}")
                    # driver.back()
                    # time.sleep(2)
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



    driver.quit()

makes = ['audi', 'bmw', 'ford', 'mercedes', 'toyota']
# for make in makes:
scrape_dubizzle_images("audi")
