import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import random



# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
USER_AGENTS = [
   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
   'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66',
   'Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36',
   'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
    # More user agents can be added here
]
SITES = {
    "Best Buy": "https://www.bestbuy.com/site/searchpage.jsp?st=",
    "Walmart": "https://www.walmart.com/search/?query=",
    "Newegg": "https://www.newegg.com/p/pl?d="
}

def get_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def fetch_data(site_name, search_url):
    session = get_session()
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    response = session.get(search_url, headers=headers, timeout=(10, 30))
    response.raise_for_status()
    return response.text

def parse_data(site_name, html):
    soup = BeautifulSoup(html, 'html.parser')
    if site_name == "Best Buy":
        product = soup.find("h4", class_="sku-header") or soup.find("h4", class_="sku-title")
        price = soup.find("div", class_="priceView-hero-price priceView-customer-price")
    elif site_name == "Walmart":
        product = soup.find("a", class_="product-title-link") or soup.find("a", class_="link-display")
        price = soup.find("span", class_="price-group") or soup.find("div", class_="price-characteristic")
    elif site_name == "Newegg":
        product = soup.find("a", class_="item-title")
        price = soup.find("li", class_="price-current")

    item_title = product.text.strip() if product else "Product not found"
    item_price = price.text.strip() if price else "Price not available"
    return site_name, item_title, item_price

def search_product(product_name):
    results = []
    for site_name, base_url in SITES.items():
        try:
            search_url = f"{base_url}{product_name.replace(' ', '+')}"
            logging.info(f"Fetching data from {site_name} for '{product_name}'")
            html = fetch_data(site_name, search_url)
            result = parse_data(site_name, html)
            results.append({"Site": result[0], "Item Title Name": result[1], "Price (USD)": result[2]})
        except requests.exceptions.HTTPError as errh:
            logging.error(f"HTTP Error occurred: {errh}")
        except requests.exceptions.ConnectionError as errc:
            logging.error(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            logging.error(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            logging.error(f"OOps: Something Else {err}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    df = pd.DataFrame(results)
    logging.info(f"\n{df}")
    df.to_csv('product_search_results.csv', index=False)

# Example product search
if __name__ == "__main__":
    product_name = input("Enter the product name to search: ")
    search_product(product_name)
