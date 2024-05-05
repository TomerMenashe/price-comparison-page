from utils import get_driver
import urllib.parse
from selenium.webdriver.common.by import By

# Define an asynchronous function to scrape Newegg for a specific product
async def scrape_newegg(product_name: str) -> dict:
    # Get a Selenium WebDriver instance
    driver = get_driver()
    
    # Construct the search URL by URL encoding the product name
    search_url = f"https://www.newegg.com/p/pl?d={urllib.parse.quote_plus(product_name)}"
    
    # Navigate to the constructed URL with the WebDriver
    driver.get(search_url)
    
    # Initialize a dictionary to store the result with default values
    result = {"price": "Price not found", "product_url": ""}

    try:
        # Find the first product link on the search result page and get its URL
        first_product_link = driver.find_element(By.CSS_SELECTOR, 'a.item-title').get_attribute('href')
        result["product_url"] = first_product_link  # Update the product URL in the result dictionary

        # Navigate to the product page
        driver.get(first_product_link)

        # Find and extract the price from the product page
        price_element = driver.find_element(By.CSS_SELECTOR, '.price-current strong')
        if price_element:
            result["price"] = f"${price_element.text}"  # Update the price in the result dictionary
    except Exception as e:
        # Handle exceptions and log any errors that occur during the scraping process
        print(f"Error finding price at Newegg: {e}")
    finally:
        # Ensure that the WebDriver is closed after the scraping process
        driver.quit()
    
    # Return the result dictionary containing the price and product URL
    return result
