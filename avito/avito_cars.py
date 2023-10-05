import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from dataclasses import dataclass, asdict
from typing import Optional

from datetime import datetime


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
BASE_URL = "https://www.avito.ma/fr/maroc/voitures/"
SEARCH_TERM = "Golf"


@dataclass
class Car:
    search_term: str
    link: str
    name: Optional[str]
    city: Optional[str]
    price: Optional[str]
    fuel_type: Optional[str]
    horse_power: Optional[str]
    transmission_system: Optional[str]
    used_car: Optional[str]
    sector: Optional[str]
    state: Optional[str]
    year_model: Optional[str]
    door_count: Optional[str]
    first_hand: Optional[str]
    origin: Optional[str]
    model: Optional[str]
    brand: Optional[str]
    milage: Optional[str]
    date_scraped: str


def load_page(url):
    response = requests.get(url, headers={'user-agent': USER_AGENT})
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def load_search_page():
    search_query = f"{SEARCH_TERM}--%C3%A0_vendre?price_min=10000"
    search_page = urljoin(BASE_URL, search_query)
    return load_page(search_page)


def get_car_listings(soup):
    listings_class = "listing"
    listings = soup.find("div", {"class": listings_class})
    listings = listings.find_all("a")
    links = [listing["href"] for listing in listings]
    return links


def get_car_details(car_url):
    soup = load_page(car_url)
    # Initialize all variables to None
    name = city = price = fuel_type = horse_power = transmission_system = used_car = ""
    sector = state = year_model = door_count = first_hand = origin = model = brand = milage = ""
    # Extract data
    try:
        name = soup.find("div", {"class": "sc-1g3sn3w-9 kvOteU"}).h1.text.strip()
        city = soup.find("span", {"class": "sc-1x0vz2r-0 iotEHk"}).text.strip()
        price = soup.find("p", {"class": "sc-1x0vz2r-0 lnEFFR sc-1g3sn3w-13 czygWQ"}).text.strip()
        about = soup.find_all("span", {"class": "sc-1x0vz2r-0 kQHNss"})
        fuel_type = about[0].text.strip()
        horse_power = about[1].text.strip()
        transmission_system = about[2].text.strip()
    except Exception as e:
        print(f"Error: {e}")
        print(f"@ {car_url}")
    try:
        about = soup.find_all("span", {"class": "sc-1x0vz2r-0 gSLYtF"})
        used_car = about[0].text.strip()
        sector = about[1].text.strip()
        state = about[2].text.strip()
        year_model = about[3].text.strip()
        door_count = about[4].text.strip()
        first_hand = about[5].text.strip()
        origin = about[6].text.strip()
        model = about[7].text.strip()
        brand = about[8].text.strip()
        milage = about[9].text.strip()
    except Exception as e:
        print(f"Error: {e}")
        print(f"@ {car_url}")
    car = Car(
        search_term=SEARCH_TERM,
        link=car_url,
        name=name,
        city=city,
        price=price,
        fuel_type=fuel_type,
        horse_power=horse_power,
        transmission_system=transmission_system,
        used_car=used_car,
        sector=sector,
        state=state,
        year_model=year_model,
        door_count=door_count,
        first_hand=first_hand,
        origin=origin,
        model=model,
        brand=brand,
        milage=milage,
        date_scraped=datetime.now().strftime('%a %d %b %Y, %I:%M%p'),
    )
    return car


def main():
    search_page = load_search_page()
    car_listings = get_car_listings(search_page)
    for car_link in car_listings:
        print(car_link)
        car = get_car_details(car_link)
        print(asdict(car))
        print("----")
        with open("avito_cars.csv", "a", encoding="utf-8") as file:
            # Write car data to CSV file
            file.write('\t'.join(asdict(car).values()) + '\n')


if __name__ == "__main__":
    main()
