import csv
from dataclasses import dataclass, asdict
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from datetime import datetime


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
BASE_URL = "https://www.ebay.com/globaldeals"


@dataclass
class Product:
    link: str
    title: str
    price: str
    date_scraped: str


def scrape_products():
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(BASE_URL, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        product_items = soup.select('[class="ebayui-dne-featured-card ebayui-dne-featured-with-padding"] [itemscope][data-listing-id] [class="dne-itemtile-detail"]')

        products_list = []

        for item in product_items:
            product_link = urljoin(BASE_URL, item.select_one('[href]')['href'])
            product_title = item.select_one('[href] span span').get_text()
            product_price = item.select_one('[itemprop="price"]').get_text()

            product = Product(product_link, product_title, product_price, datetime.now().strftime('%a %d %b %Y, %I:%M%p'))
            products_list.append(product)

        return products_list

    else:
        print("Failed to fetch the webpage")
        return []


def save_to_csv(products_list):
    if products_list:
        with open("ebay_deals.csv", "a", encoding="utf-8") as file:
            for product in products_list:
                file.write('\t'.join(asdict(product).values()) + '\n')


if __name__ == "__main__":
    products = scrape_products()
    if products:
        save_to_csv(products)
        print("Data saved to products.csv")
    else:
        print("No products found or an error occurred during scraping.")
