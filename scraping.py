import bs4
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Let's make this all a function so we can loop through it for all 50 pages of the book site
def bookscraper(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Scrapes the title of each book
    titles = []
    for title in soup.find_all('div', class_ = "image_container"):
        img = title.find('img', alt=True)
        # print(img['alt'])
        titles.append(img['alt'])

    # Scrapes the price of each book (stored as a string in this case)
    prices = []
    for price in soup.find_all('p', class_ = 'price_color'):
        # print(price.text)
        prices.append(price.text.replace('£',''))

    # Add scraped values into a dictionary/dataframe using Pandas
    books = pd.DataFrame({
        "Title":titles,
        "Price":prices,
    })

    # Convert prices to float
    books.Price = books.Price.astype(float)
    return(books)

# Let's make develop a list of all the URL's that we want to scrape using the proper form

# All URLs are of the following form:
# url = 'https://books.toscrape.com/catalogue/category/books_1/index.html'
# url = 'https://books.toscrape.com/catalogue/category/books_1/page-29.html'

url_list = []
for i in range(1,51):
    url_list.append('https://books.toscrape.com/catalogue/category/books_1/page-' + str(i) + '.html')

# Generate a loop to call on function necessary number of times
master_books = pd.DataFrame({})
for x in range(0,len(url_list)-1):
    master_books = master_books.append(bookscraper(url_list[x]), ignore_index = True)

master_books.to_csv('Books_Scraped.csv')