from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait as wait 
from selenium.webdriver.support import expected_conditions as EC 
import pandas as pd
from database import store_db
import gspread

# Global var to reset page each time
next_page = ''

# Website to scrape
url = 'https://www.amazon.com'

# Set up Selenium driver
options = webdriver.ChromeOptions()
# options.add_argument('headless')

def scrape_amazon(keywordArg, max_pages):
    page_num = 1
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    driver.get(url)
    driver.implicitly_wait(5)

    # Assign keyword to search
    keyword = keywordArg

    # Create WebElement for a search box
    search_box = driver.find_element(By.ID, 'twotabsearchtextbox')

    # Type in the keyword in searchbox
    search_box.send_keys(keyword)

    # Create WebElement for a search button
    search_button = driver.find_element(By.ID, 'nav-search-submit-button')
    search_button.click()
    
    # Wait for the page to download
    driver.implicitly_wait(5)

    # Search multiple pages
    while page_num <= max_pages:
        # Scrape page and store in database
        scrape_page(driver)
        # Go to next page using button's href
        driver.get(next_page)
        driver.implicitly_wait(5)
        page_num += 1
    
    # Quit the driver after finishing scraping
    driver.quit()

def scrape_page(driver):
    # Connect to Google Spreadsheets
    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open("Amazon Listing Scraper")

    # Store scraped data
    product_name = []
    product_asin = []
    product_price = []
    product_ratings = []
    product_ratings_num = []
    product_link = []

    # Create a WebElement using XPATH equal to the div we want to scrape from
        # Allow Selenium to wait at most 10 seconds until it can locate elements
        # Prevent NoSuchElementException
        # Replaces find_elements
    items = wait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))

    # Extract data from WebElements
        # Use item and not driver since we're now looking for sub-elements of the WebElement
        # Also why we start xpath using .// instead of // to show that we're only looking at the item instead of the entire page

    for item in items:
        name = item.find_element(By.XPATH, './/span[@class="a-size-medium a-color-base a-text-normal"]')
        product_name.append(name.text)

        data_asin = item.get_attribute("data-asin")
        product_asin.append(data_asin)

        # Use find_elements for price since not all items will have a price
        # This is so it can return an empty list if there is none
            # Opposed to find_element, which finds a WebElement, and will throw an error if empty

        # Dollars
        whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
        
        # Cents
        fraction_price = item.find_elements(By.XPATH, './/span[@class="a-price-fraction"]')

        # Remove commas from prices > 1000
        if whole_price != [] and fraction_price != []:
            price = '.'.join([whole_price[0].text.replace(",",""), fraction_price[0].text])
        else:
            price = 0
        product_price.append(price)
        
        # Find ratings box and create a WebElement
        ratings_box = item.find_elements(By.XPATH, './/div[@class="a-row a-size-small"]/span')

        # Find ratings and ratings_num
        if ratings_box != []:
            ratings = ratings_box[0].get_attribute('aria-label')
            ratings_num = ratings_box[1].get_attribute('aria-label')
        else:
            ratings = 0
            ratings_num = 0

        product_ratings.append(ratings)
        product_ratings_num.append(str(ratings_num))

        # Find details link for the item
        link = item.find_element(By.XPATH, './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]').get_attribute("href")
        product_link.append(link)

    # Create WebElement for next page
    global next_page
    next_page = driver.find_element(By.XPATH, './/a[@class="s-pagination-item s-pagination-button"]').get_attribute("href")

    # Create a list that joins all lists together
    joinedTable = list(zip(product_asin, product_name, product_price, product_ratings, product_ratings_num, product_link))
    
    # Store page's scraped data to google spreadsheets
    for row in joinedTable:
        sh.sheet1.append_row(row)

    # Store page's scraped data into database
    store_db(product_asin, product_name, product_price, product_ratings, product_ratings_num, product_link)


if __name__=='__main__':
    scrape_amazon('lawnmower', 1)