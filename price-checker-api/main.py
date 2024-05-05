from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from asyncio import gather, wait_for, TimeoutError
from scraper_bestbuy import scrape_bestbuy
from scraper_walmart import scrape_walmart
from scraper_newegg import scrape_newegg
from urllib.parse import unquote
import asyncio

# Creating an instance of the FastAPI application
app = FastAPI()

# Configuring CORS (Cross-Origin Resource Sharing) middleware
# Allows requests from any origin, which is useful for API accessibility from different domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Accept all origins
    allow_credentials=True,
    allow_methods=["*"],  # Accept all methods
    allow_headers=["*"],  # Accept all headers
)

# Define an endpoint that accepts a GET request
@app.get("/api/compare-prices")
async def get_prices(product_name: str):
    try:
        # Decoding the URL-encoded product name
        decoded_string = unquote(product_name)

        # Using asyncio gather to run all scraper functions concurrently
        # and setting an overall timeout of 30 seconds for all to complete
        results = await wait_for(gather(
            scrape_bestbuy(decoded_string),
            scrape_newegg(decoded_string),
            scrape_walmart(decoded_string)
        ), timeout=30)

        # Extracting prices and URLs from the results of scrapers
        bestbuy_price = results[0]["price"]
        bestbuy_url = results[0]["product_url"]
        newegg_price = results[1]["price"]
        newegg_url = results[1]["product_url"]
        walmart_price = results[2]["price"]
        walmart_url = results[2]["product_url"]
        
        # Returning a structured response with prices and product URLs for each store
        return {
            "BestBuy": {"price": bestbuy_price, "product_url": bestbuy_url},
            "Newegg": {"price": newegg_price, "product_url": newegg_url},
            "Walmart": {"price": walmart_price, "product_url": walmart_url}
        }
    except TimeoutError:
        # Return a 408 error if the timeout is exceeded
        return HTTPException(status_code=408, detail="Request timeout, one or more scrapers did not finish in time.")
    except Exception as e:
        # Handle other exceptions with a 500 server error response
        print(f"An error occurred: {str(e)}")
        return HTTPException(status_code=500, detail=str(e))
