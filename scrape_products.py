from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote_plus
import time
import random

def get_driver():
    """Function to initiate a Selenium WebDriver."""
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument('disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-application-cache')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-dev-shm-usage")
    # Randomly choose a user-agent
    user_agents = [
        #'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        #'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
    ]
    options.add_argument(f'user-agent={random.choice(user_agents)}')
    # Specify the path to chromedriver.exe
    service = Service(executable_path='/opt/homebrew/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def search_bestbuy(driver, product_name):
    """Search for a product on Best Buy using Selenium."""
    safe_product_name = quote_plus(product_name)
    url = f"https://www.bestbuy.com/site/searchpage.jsp?st={safe_product_name}&intl=nosplash"
    driver.get(url)
    time.sleep(5)  # Let the page load completely
    price = "Price not found"
    try:
        # Find the first product link and click on it
        product_link = driver.find_element(By.CSS_SELECTOR, '.sku-item')
        product_link.click()

        # Wait until the price element is present on the product page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.priceView-hero-price'))
        )

        # Extract the price from the product page
        price_element = driver.find_element(By.CSS_SELECTOR, '.priceView-hero-price')
        if price_element:
            price = price_element.text.strip()
    except Exception as e:
        print("Error finding price at Best Buy:", e)
    return url, price

def search_walmart(driver, product_name):
    """Search for a product on Walmart using Selenium and extract the price."""
    safe_product_name = quote_plus(product_name)
    url = f"https://www.walmart.com/search/?query={safe_product_name}"
    driver.get(url)
    time.sleep(5)  # Let the page load completely
    price = "Price not found"
    try:
        # Wait for the search results to load and click the first product link
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.search-result-gridview-item-wrapper'))
        )
        product_links = driver.find_elements(By.CSS_SELECTOR, '.search-result-gridview-item-wrapper a.link-identifier')
        if product_links:
            product_links[0].click()  # Click on the first product link

            # Wait for the price element on the product page
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span[itemprop="price"]'))
            )
            price_element = driver.find_element(By.CSS_SELECTOR, 'span[itemprop="price"]')
            if price_element:
                price = price_element.text.strip()
    except Exception as e:
        print("Error finding price at Walmart:", e)
    return url, price







def search_newegg(driver, product_name):
    """Search for a product on Newegg using Selenium."""
    safe_product_name = quote_plus(product_name)
    url = f"https://www.newegg.com/p/pl?d={safe_product_name}"
    driver.get(url)
    time.sleep(5)  # Let the page load completely
    price = "price Not found"
    try:
        price_elements = driver.find_elements(By.CSS_SELECTOR, 'li.price-current')
        if price_elements:
            # Assuming the first product's price is the required one
            price = price_elements[0].text.strip().split()[0]  # Extract only the price part
    except Exception as e:
        print("Error finding price at Newegg:", e)
    return url, price

def main():
    driver = get_driver()
    product_name = input("Enter the name of the product you want to search: ")

    print("\nSearching Bestbuy...")
    bestbuy_results = search_bestbuy(driver, product_name)
    print("\nBestbuy URL: " + bestbuy_results[0])
    print("Price: " + (bestbuy_results[1] or "No results found."))

    print("\nSearching Walmart...")
    walmart_results = search_walmart(driver, product_name)
    print("\nWalmart URL: " + walmart_results[0])
    print("Price: " + (walmart_results[1] or "No results found."))

    print("\nSearching Newegg...")
    newegg_results = search_newegg(driver, product_name)
    print("\nNewegg URL: " + newegg_results[0])
    print("Price: " + (newegg_results[1] or "No results found."))

    # Close the driver after the searches
    driver.quit()

if __name__ == "__main__":
    main()
