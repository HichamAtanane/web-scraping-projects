from datetime import datetime
from urllib.parse import urljoin
from dataclasses import dataclass, asdict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException


BASE_URL = "https://www.amazon.com/gp/goldbox"
BASE_PRODUCT_URL = "https://www.amazon.com/dp/"


@dataclass
class ProductDeal:
    link: str
    title: str
    deal_badge: str
    deal_price: str
    list_price: str
    date_scraped: str


def main():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    with webdriver.Chrome(options=options) as driver:
        driver.maximize_window()
        driver.get(BASE_URL)
        products = driver.find_elements(
                        by=By.CSS_SELECTOR,
                        value='[aria-label="Enterting Carousel Tile"][data-csa-c-channel="Amazon Live Deals"]'
                    )
        for product in products:
            asin = product.get_attribute("data-csa-c-item-id").split("asin.")[-1]
            product_link = urljoin(BASE_PRODUCT_URL, asin)
            title = product.find_element(by=By.CSS_SELECTOR, value='div[title]').get_attribute("title")

            try:
                deal_badge = product.find_element(by=By.CSS_SELECTOR, value='[data-id="DealBadge"] span').text
            except NoSuchElementException:
                deal_badge = "0% off"

            try:
                deal_price = product.find_element(by=By.CSS_SELECTOR, value='[data-id="DealPrice"]') \
                                    .get_attribute("aria-label") \
                                    .split("$")[-1]
                list_price = product.find_element(by=By.CSS_SELECTOR, value='[data-id="ListPrice"]') \
                                    .get_attribute("aria-label") \
                                    .split("$")[-1]
            except NoSuchElementException:
                deal_price = "na"
                list_price = "na"

            product = asdict(ProductDeal(link=product_link,
                                         title=title,
                                         deal_badge=deal_badge,
                                         deal_price=deal_price,
                                         list_price=list_price,
                                         date_scraped=datetime.now().strftime('%a %d %b %Y, %I:%M%p'),
                                         )
                             )
            print(product)

            with open("amazon_deals.csv", "a", encoding="utf-8") as amazon_deals:
                amazon_deals.write('\t'.join(product.values()) + '\n')


if __name__ == "__main__":
    main()






