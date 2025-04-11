import time
import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

def scrape_product_details(driver):
    product = {}
    try:
        name_element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "productTitle")))
        product['name'] = name_element.text.strip()
    except Exception as e:
        print("Error scraping product name:", e)
        product['name'] = None
    try:
        description_element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "feature-bullets")))
        product['description'] = description_element.text.strip()
    except Exception as e:
        print("Error scraping product description:", e)
        product['description'] = None
    return product

def extract_image_urls(driver):
    urls = []
    try:
        main_image_element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='imgTagWrapperId']//img")))
        urls.append(main_image_element.get_attribute('src'))
    except Exception as e:
        print("Error extracting main image URL:", e)
    return urls

def scrape_product_reviews(driver):
    reviews = []
    
    try:
        reviews_link = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(@id, 'averageCustomerReviews')]")))
        reviews_link.click()
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@id='reviewsMedley']")))
        review_elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@data-hook='review']")))
        for review_element in review_elements:
            review = {}
            review['review'] = review_element.find_element(By.XPATH, ".//span[@data-hook='review-body']").text.strip()
            review['rating'] = review_element.find_element(By.XPATH, ".//span[@class='a-icon-alt']").get_attribute('innerText').split()[0]
            reviews.append(review)
    except Exception as e:
        print("Error scraping product reviews:", e)
    
    return reviews

def handle_pagination(driver):
    try:
        next_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='search']//*[contains(@class, 's-result-item')]/div/div/span/a[3]")))
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        time.sleep(0.5)
        next_button.click()
        return True
    except Exception as e:
        print("Error clicking next button:", e)
        return False

user_agent = UserAgent().random

chrome_options = Options()
chrome_options.add_argument(f'user-agent={user_agent}')  # Set user agent
chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # Disable automation control
driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://www.amazon.com")

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "twotabsearchtextbox")))

    time.sleep(random.uniform(2, 4))  

    # List of XPaths
    xpath_lists = [
        [
            "//*[contains(@id, 'nav-hamburger-menu')]/i",   # All
            "//*[contains(@id, 'hmenu-content')]/ul[position()=1]/li[position()=11]/a[position()=1]", # See All
            "//*[@id='hmenu-content']//ul[contains(@class, 'hmenu-visible')]//li[position()=6]/a/i",   # Men's Fashion
            "//*[@id='hmenu-content']//ul[contains(@class, 'hmenu-visible')]/li[3]/a",   # Clothing
            "//*[@id='search']//div[contains(@class, 's-result-item')][3]//h2/a/span" # Product
        ],
        [
            "//*[contains(@id, 'nav-hamburger-menu')]/i",   # All
            "//*[contains(@id, 'hmenu-content')]/ul[position()=1]/li[position()=11]/a[position()=1]", # See All
            "//*[@id='hmenu-content']//ul[contains(@class, 'hmenu-visible')]//li[position()=6]/a/i",   # Men's Fashion
            "//*[@id='hmenu-content']/ul[41]/li[4]/a", # Shoes
            "//*[@id='search']//div[contains(@class, 's-result-item')][3]//h2/a/span" # Product
        ],
        [
            "//*[contains(@id, 'nav-hamburger-menu')]/i",   # All
            "//*[contains(@id, 'hmenu-content')]/ul[position()=1]/li[position()=11]/a[position()=1]", # See All
            "//*[@id='hmenu-content']//ul[contains(@class, 'hmenu-visible')]//li[position()=6]/a/i",   # Men's Fashion
            "//*[@id='hmenu-content']//ul[contains(@class, 'hmenu-visible')]//li[position()=5]/a", # Watches
            "//*[@id='search']//div[contains(@class, 's-result-item')][2]//h2/a/span" # Product
        ],
        [
            "//*[contains(@id, 'nav-hamburger-menu')]/i",   # All
            "//*[contains(@id, 'hmenu-content')]/ul[position()=1]/li[position()=11]/a[position()=1]", # See All
            "//*[@id='hmenu-content']//ul[contains(@class, 'hmenu-visible')]//li[position()=6]/a/i",   # Men's Fashion
            "//*[@id='hmenu-content']//ul[contains(@class, 'hmenu-visible')]//li[position()=6]/a", # Accessories
            "//*[@id='search']//div[contains(@class, 's-result-item')][2]//h2/a/span" # Product
        ],
        [
            "//*[contains(@id, 'nav-hamburger-menu')]/i",   # All
            "//*[contains(@id, 'hmenu-content')]/ul[position()=1]/li[position()=11]/a[position()=1]", # See All
            "//*[@id='hmenu-content']//ul/ul/li[position()=2]/a",   # Automotive
            "//*[@id='hmenu-content']//ul[contains(@class, 'hmenu-visible')]//li[position()=3]/a", # Car Care
            "//*[@id='search']//div[contains(@class, 's-result-item')][2]//h2" # Product
        ]
    ]

    data_list = []

    for xpath_list in xpath_lists:
        for xpath in xpath_list:
            try:
                button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                driver.execute_script("arguments[0].scrollIntoView();", button)
                time.sleep(0.5)  # Small delay after scrolling
                driver.execute_script("window.scrollBy(0, -150);")  # Scroll up a bit to avoid interception
                button.click()
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "some_element_id")))  # Increase timeout
                time.sleep(random.uniform(2, 4))  # Random delay between 2 to 4 seconds

                count = 0
                while count < 1000:
                    product = scrape_product_details(driver)
                    image_urls = extract_image_urls(driver)
                    reviews = scrape_product_reviews(driver)
                    data = {
                        'product': product,
                        'image_urls': image_urls,
                        'reviews': reviews
                    }
                    data_list.append(data)  # Add data to the list
                    count += 1
                    
                    if not handle_pagination(driver):
                        break  # Exit loop if there is no next button
                
            except ElementClickInterceptedException as e:
                print(f"Error clicking on button: {str(e)}")
            except TimeoutException as te:
                print(f"Timeout while processing: {str(te)}")
            except Exception as ex:
                print(f"Error while processing: {str(ex)}")


except TimeoutException as te:
    print("Timeout while waiting for page to load:", te)

finally:
    with open('product_data.json', 'w') as f:
        json.dump(data_list, f, indent=4)
    while(True):
        i = 0
        i = i+1
    #driver.quit()
