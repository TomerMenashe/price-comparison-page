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

def search_bestbuy(safe_product_name):
    url = f"https://www.bestbuy.com/site/searchpage.jsp?st={safe_product_name}&intl=nosplash"
    headers = get_headers()  # Get random User-Agent and other headers
    response = requests.get(url, headers=headers)
    print(response.status_code)
    #print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    price = "price Not found"
    # Look for the price within the specified container
    price_container = soup.find('div', class_='priceView-hero-price priceView-customer-price')
    if price_container:
        price_span = price_container.find('span', {'aria-hidden': 'true'})
        if price_span:
            price = price_span.get_text().strip()

    return url, price
    

def search_walmart(safe_product_name):
    url = f"https://www.walmart.com/search/?query={safe_product_name}"
    response = requests.get(url)
    print(response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Assuming product names are in <a> tags with data-automation-id "title"
    products = soup.find_all('a', {'data-automation-id': 'title'})
    return url, [product.get_text().strip() for product in products]

def search_newegg(safe_product_name):
    url = f"https://www.newegg.com/p/pl?d={safe_product_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Assuming product names are in <a> tags with class "item-title"
    products = soup.find_all('a', class_='item-title')
    return url, [product.get_text().strip() for product in products]

def main():
    product_name = input("Enter the name of the product you want to search: ")
    safe_product_name = quote_plus(product_name)  # URL encode once here

    print("\nSearching Bestbuy...")
    bestbuy_results = search_bestbuy(safe_product_name)
    print("\n Bestbuy url: " + bestbuy_results[0]) 
    print("Price: ")
    print(bestbuy_results[1] or "No results found.")
    
  #  print("\nSearching Walmart...")
   # walmart_results = search_walmart(safe_product_name)
    #print("\n walmart url: " + walmart_results[0]) 
    #print("Walmart Results:")
    #print(walmart_results[1] or "No results found.")
    
  #  print("\nSearching Newegg...")
   # newegg_results = search_newegg(safe_product_name)
    #print("\n newegg url: " + newegg_results[0]) 
    #print("Newegg Results:")
    #print(newegg_results[1] or "No results found.")

if __name__ == "__main__":
    main()
