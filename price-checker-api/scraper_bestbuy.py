from utils import get_driver
from urllib.parse import quote_plus
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define an asynchronous function to scrape Best Buy for a given product
async def scrape_bestbuy(product_name: str) -> dict:
    # Get the Selenium WebDriver instance from utility functions
    driver = get_driver()

    # URL encode the product name to safely include it in a URL
    safe_product_name = quote_plus(product_name)

    # Construct the URL for searching the product on Best Buy's website
    url = f"https://www.bestbuy.com/site/searchpage.jsp?st={safe_product_name}&intl=nosplash"
    
    # Navigate to the URL using Selenium
    driver.get(url)

    # Initialize the result dictionary with default values
    result = {"price": "Price not found", "product_url": ""}

    try:
        # Wait until the product link is clickable, then click on it
        product_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.sku-title'))
        )
        product_link.click()

        # Wait until the price element is present on the new product page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.priceView-hero-price'))
        )
        # Store the current URL as the product URL
        result["product_url"] = driver.find_element(By.XPATH, './/a').get_attribute('href')
        
        
        # Find the element that contains the price
        price_element = driver.find_element(By.CSS_SELECTOR, '.priceView-hero-price')
        if price_element:
            # Extract the text, strip whitespace, and assume the price is the first line if there are multiple lines
            result["price"] = price_element.text.strip().split('\n')[0]
    except Exception as e:
        # Log any errors encountered during scraping
        print(f"Error finding price at Best Buy: {e}")
    finally:
        # Ensure the WebDriver is closed after the scraping
        driver.quit()
    
    # Return the result dictionary
    return result
