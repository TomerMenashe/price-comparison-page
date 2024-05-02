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
    """ Function to construct headers with a specific User-Agent for consistent web scraping """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/'
    }
    return headers


def get_first_product_link(soup):
    """ Extract the first product link from the search results page """
    # Locating the first product link by searching within divs with a specific data-testid that seems to contain the product links
    item_stack = soup.find("div", attrs={"data-testid": "item-stack"})
    if item_stack:
        product_link = item_stack.find("a")
        if product_link and 'href' in product_link.attrs:
            first_product_link = product_link['href']
            # Check if the URL is already complete
            if not first_product_link.startswith('http'):
                first_product_link = 'https://www.walmart.com' + first_product_link
            print("First product link: " + first_product_link)  # for debugging
            return first_product_link
    print("No first product link found")
    return None


def search_walmart(safe_product_name):
    url = f"https://www.walmart.com/search/?query={safe_product_name}"
    print("url: " + url)  # for debuging
    headers = get_headers()  # Get random User-Agent and other headers
    print("Using headers:", headers)  # Print the headers being used
    response = requests.get(url, headers=headers)
    print("Search page status code:", response.status_code)  # Debug
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        first_product_link = get_first_product_link(soup)
        print("first product link: " + first_product_link) # for debuging
        if first_product_link:
            return get_product_details(first_product_link)
        else:
            return "althought status code is 200", "and we in the if cond", "the get product link or details failed"
    else:
        print("Failed to fetch search page, status code:", response.status_code)
        return "getting the ", "main web url", "failed"

def get_product_details(url):
    """ Fetch the product details from the product's page """
    headers = get_headers()
    print("Using headers (get_product_details):", headers)  # Print the headers being used
    response = requests.get(url, headers=headers)
    print("Product details page status code:", response.status_code)  # Debug
    soup = BeautifulSoup(response.text, 'html.parser')
    # Writing the prettified HTML to a file
    with open('output.html', 'w', encoding='utf-8') as file:
        file.write(soup.prettify())
    price = "Price Not found"
    title = "Title Not found"
    site = "Walmart.com"

    # Extract price
    price_wrap = soup.find('div', {'data-testid': 'price-wrap'})
    if price_wrap:
        print("Found price-wrap div")  # Debug: Confirm price-wrap div is found
        price_info = price_wrap.find('span', itemprop='price')
        if price_info:
            price_spans = price_info.find_all('span')
            price_parts = [span.text for span in price_spans if span.text.strip() != '']
            price = ''.join(price_parts).strip()
            print(f"Extracted price: {price}")  # Debug: Show extracted price
        else:
            print("Price info not found")  # Debug: More specific message
    else:
        print("Price wrap not found")  # Debug: Confirm price-wrap div is not found

    # Extract title from the <title> tag
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.text.strip()
        # Remove " - Walmart.com" from the title
        title = title.replace(' - Walmart.com', '')
        print("Found title:", title)  # Debug
    else:
        print("Title not found")  # Debug


    return price, title, site

def main():
    product_name = input("Enter the name of the product you want to search: ")
    safe_product_name = quote_plus(product_name)  # URL encode once here
    print("safe product name: "  + str(safe_product_name)) # for debuging

    print("\nSearching Walmart...")
    result = search_walmart(safe_product_name)
    if result and len(result) == 3:
        price, title, site = result
        print(f"\nSite: {site}")
        print(f"Title: {title}")
        print(f"Price: {price}")
    else:
        error_message = result[1] if len(result) == 2 else "Unexpected error"
        print(error_message)

if __name__ == "__main__":
    main()
