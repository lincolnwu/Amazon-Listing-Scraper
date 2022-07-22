from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait as wait 
from selenium.webdriver.support import expected_conditions as EC 
import pandas as pd
import psycopg2
import getpass 
import configparser 

# Global var to reset page each time
next_page = ''


# Website to scrape
url = 'https://www.amazon.com'

# Set up Selenium driver
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
driver.get(url)

driver.implicitly_wait(5)

# Assign keyword to search
keyword = "wireless charger"

# Create WebElement for a search box
search_box = driver.find_element(By.ID, 'twotabsearchtextbox')

# Type in the keyword in searchbox
search_box.send_keys(keyword)

# Create WebElement for a search button
search_button = driver.find_element(By.ID, 'nav-search-submit-button')
search_button.click()
 
# Wait for the page to download
driver.implicitly_wait(5)


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
# print(items)

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

    if whole_price != [] and fraction_price != []:
        price = '.'.join([whole_price[0].text, fraction_price[0].text])
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

# Quit the driver after finishing scraping
driver.quit()

# final = [product_name, product_asin, product_price, product_ratings, product_ratings_num, product_link]
# df = pd.DataFrame(final, columns=['Product Name', 'ASIN', 'Price', 'Rating', 'Number of Ratings', 'Link'])
# print(df)
result = {
    'Product Name' : product_name,
    'ASIN' : product_asin,
    'Price' : product_price,
    'Ratings' : product_ratings,
    'Number of Ratings' : product_ratings_num,
    'Product Link' : product_link
}
df = pd.DataFrame(result)
print(df)