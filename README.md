# Amazon-Listing-Scraper
Automated web scraper that gathers information on product listings based on the user’s search

## Description
Web scraper that takes an input and returns product listings from Amazon. A listing includes the product's ASIN, name, price, rating/number of ratings, and
the link to the product. In addition, the user can choose to store the scraped results in Google Spreadsheets and/or a PostgreSQL database. 

## How to Run the Project
1. Clone the repository with `git clone`
2. Install dependencies using `pip install selenium gspread tkinter`
3. Start app with `python3 amazon.py`

## Setting up PostgreSQL
1. Create a file named `database.ini`
2. Enter credentials in the following format:
 `[postgresql]
  host=localhost
  dbname=[your database name]
  user=[your username]
  password=[your password]`

## Setting up Google Spreadsheets
1. Enable Google Drive and Google Spreadsheets API at https://console.cloud.google.com/
2. Create a new project and service account
3. Download the service account's key credentials information as a JSON and name it as `credentials.json`. The program will read any authentication information from this file in the project directory.
4. Create a new Google Spreadsheet with any title. Ex: `Amazon Listing Scraper`
5. Input the name of the spreadsheet on the line containing: `sh = gc.open("Amazon Listing Scraper")`
6. Share this spreadsheet with the service account's email. 

## Technologies
- Selenium
- Google Spreadsheets API
- PostgreSQL
- Tkinter
