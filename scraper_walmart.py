from utils import get_driver
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_and_get_walmart_price(product_name):
    driver = get_driver()
    search_url = f"https://www.walmart.com/search/?query={urllib.parse.quote_plus(product_name)}"
    driver.get(search_url)
    price = "Price not found"
    try:
        # Wait for the search results to load and ensure the items are visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[class="f2"]'))
        )
        price_element = driver.find_element(By.CSS_SELECTOR, '[class="f2"]')
        price = f"${price_element.text.strip()}"

    except Exception as e:
        print(f"Error during Walmart price extraction: {e}")
    finally:
        driver.quit()
    return price
