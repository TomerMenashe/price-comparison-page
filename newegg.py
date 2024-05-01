import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import random

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
]

def get_headers():
    """ Function to randomly select a User-Agent and construct headers """
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/'
    }
    return headers

def get_first_product_link(soup):
    """ Extract the first product link from the search results page """
    search_results = soup.find_all("a", class_="item-title")
    if search_results:
        first_product_link = search_results[0]['href']
        print("first product link: " + first_product_link) # for debuging
        return first_product_link
    return None

def search_newegg(safe_product_name):
    url = f"https://www.newegg.com/p/pl?d={safe_product_name}"
    print("url: " + url)  # for debuging
    headers = get_headers()  # Get random User-Agent and other headers
    response = requests.get(url, headers=headers)
    print(response.status_code)  # for debuging
    soup = BeautifulSoup(response.text, 'html.parser')
    first_product_link = get_first_product_link(soup)
    if first_product_link:
        return get_product_details(first_product_link)
    else:
        return None, "No results found"

def get_product_details(url):
    """ Fetch the product details from the product's page """
    headers = get_headers()
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    price = "Price Not found"
    title = "Title Not found"
    site = "Newegg.com"

    # Extract price
    price_container = soup.find('li', class_='price-current')
    if price_container:
        price_strong = price_container.find('strong')
        price_sup = price_container.find('sup')
        if price_strong and price_sup:
            price = price_strong.text.strip() + price_sup.text.strip()

    # Extract title
    title_container = soup.find('h1', class_='product-title')
    if title_container:
        title = title_container.text.strip()

    return price, title, site

def main():
    product_name = input("Enter the name of the product you want to search: ")
    safe_product_name = quote_plus(product_name)  # URL encode once here

    print("\nSearching Newegg...")
    price, title, site = search_newegg(safe_product_name)
    print(f"\nSite: {site}")
    print(f"Title: {title}")
    print(f"Price: {price}")

if __name__ == "__main__":
    main()
