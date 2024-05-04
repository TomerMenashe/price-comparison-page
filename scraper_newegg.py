from utils import get_driver
import urllib.parse
from selenium.webdriver.common.by import By

def search_and_get_newegg_price(product_name):
    driver = get_driver()
    search_url = f"https://www.newegg.com/p/pl?d={urllib.parse.quote_plus(product_name)}"
    driver.get(search_url)
    try:
        # Logic to select the first product link (adjust selector as needed)
        first_product_link = driver.find_element(By.CSS_SELECTOR, 'a.item-title').get_attribute('href')
        driver.get(first_product_link)

        # Extract price
        price_element = driver.find_element(By.CSS_SELECTOR, '.price-current strong')
        price = f"${price_element.text}"
    finally:
        driver.quit()
    return price
