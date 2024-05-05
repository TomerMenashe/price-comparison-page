from utils import get_driver
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

async def scrape_walmart(product_name: str) -> dict:
    driver = get_driver()
    search_url = f"https://www.walmart.com/search/?query={urllib.parse.quote_plus(product_name)}"
    driver.get(search_url)
    result = {"price": "Price not found", "product_url": ""}
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[class="f2"]'))
        )
        price_element = driver.find_element(By.CSS_SELECTOR, '[class="f2"]')
        if price_element:
            result["price"] = f"${price_element.text.strip()}"
            # Capture the first product link
            first_product_link = driver.find_element(By.CSS_SELECTOR, '[class="absolute w-100 h-100 z-1 hide-sibling-opacity z-2"]').get_attribute('href')
            result["product_url"] = first_product_link
    except Exception as e:
        print(f"Error during Walmart price extraction: {e}")
    finally:
        driver.quit()
    return result
