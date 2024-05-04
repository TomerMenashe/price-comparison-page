from utils import get_driver
import urllib.parse
from selenium.webdriver.common.by import By

def scrape_newegg(product_name: str) -> str:
    driver = get_driver()
    search_url = f"https://www.newegg.com/p/pl?d={urllib.parse.quote_plus(product_name)}"
    driver.get(search_url)
    price = "Price not found"
    try:
        # Logic to select the first product link
        first_product_link = driver.find_element(By.CSS_SELECTOR, 'a.item-title').get_attribute('href')
        driver.get(first_product_link)

        # Extract price
        price_element = driver.find_element(By.CSS_SELECTOR, '.price-current strong')
        if price_element:
            price = f"${price_element.text}"
    except Exception as e:
        print(f"Error finding price at Newegg: {e}")
    finally:
        driver.quit()
    return price
