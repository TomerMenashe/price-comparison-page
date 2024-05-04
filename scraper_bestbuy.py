from utils import get_driver
from urllib.parse import quote_plus
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_and_get_bestbuy_price(product_name):
    driver = get_driver()
    safe_product_name = quote_plus(product_name)
    url = f"https://www.bestbuy.com/site/searchpage.jsp?st={safe_product_name}&intl=nosplash"
    driver.get(url)
    time.sleep(5)  # Let the page load completely
    price = "Price not found"
    try:
        # Find the first product link and click on it
        product_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.sku-item'))
        )
        product_link.click()

        # Wait until the price element is present on the product page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.priceView-hero-price'))
        )

        # Extract the price from the product page
        price_element = driver.find_element(By.CSS_SELECTOR, '.priceView-hero-price')
        if price_element:
            price_text = price_element.text.strip()
            # Assuming the first line is always the current price
            price = price_text.split('\n')[0]  # Split by newline and get the first item
            
    except Exception as e:
        print(f"Error finding price at Best Buy: {e}")
    finally:
        driver.quit()
    return price
