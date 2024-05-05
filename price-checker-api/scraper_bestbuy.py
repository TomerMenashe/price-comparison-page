from utils import get_driver
from urllib.parse import quote_plus
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

async def scrape_bestbuy(product_name: str) -> dict:
    driver = get_driver()
    safe_product_name = quote_plus(product_name)
    url = f"https://www.bestbuy.com/site/searchpage.jsp?st={safe_product_name}&intl=nosplash"
    driver.get(url)
    time.sleep(5)  # Let the page load completely
    result = {"price": "Price not found", "product_url": ""}
    try:
        product_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.sku-title'))
        )
        product_link.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.priceView-hero-price'))
        )
        result["product_url"] = driver.current_url  # Get the URL after clicking
        price_element = driver.find_element(By.CSS_SELECTOR, '.priceView-hero-price')
        if price_element:
            result["price"] = price_element.text.strip().split('\n')[0]  # Assuming the price is the first line
    except Exception as e:
        print(f"Error finding price at Best Buy: {e}")
    finally:
        driver.quit()
    return result