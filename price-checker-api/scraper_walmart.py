from utils import get_driver
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define an asynchronous function to scrape Walmart for a specific product
async def scrape_walmart(product_name: str) -> dict:
    # Get a Selenium WebDriver instance from utility functions
    driver = get_driver()
    
    # Construct the search URL by URL encoding the product name
    search_url = f"https://www.walmart.com/search/?query={urllib.parse.quote_plus(product_name)}"
    
    # Navigate to the constructed URL using the WebDriver
    driver.get(search_url)
    
    # Initialize a result dictionary with default values
    result = {"price": "Price not found", "product_url": ""}

    try:
        # Wait until all elements with the specified class are present in the DOM
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[class="f2"]'))
        )

        # Find the price element using its CSS class and extract the text as price
        price_element = driver.find_element(By.CSS_SELECTOR, '[class="f2"]')
        if price_element:
            result["price"] = f"${price_element.text.strip()}"  # Format price with dollar sign
            
            # Find the first product link on the page and capture its href attribute
            first_product_link = driver.find_element(By.CSS_SELECTOR, '[class="absolute w-100 h-100 z-1 hide-sibling-opacity z-2"]').get_attribute('href')
            result["product_url"] = first_product_link  # Update the product URL in the result dictionary
    except Exception as e:
        # Handle exceptions and log any errors that occur during the scraping process
        print(f"Error during Walmart price extraction: {e}")
    finally:
        # Ensure that the WebDriver is closed after the scraping process to free up resources
        driver.quit()
    
    # Return the result dictionary containing the price and product URL
    return result
