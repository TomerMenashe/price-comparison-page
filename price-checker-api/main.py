from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from asyncio import gather, wait_for, TimeoutError
from scraper_bestbuy import scrape_bestbuy
from scraper_walmart import scrape_walmart
from scraper_newegg import scrape_newegg
from urllib.parse import unquote
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/compare-prices")
async def get_prices(product_name: str):
    try:
        decoded_string = unquote(product_name)
        print(decoded_string)
        # Setting an overall timeout for all scraper tasks
        bestbuy_price, newegg_price, walmart_price = await wait_for(gather(
            scrape_bestbuy(decoded_string),
            scrape_newegg(decoded_string),
            scrape_walmart(decoded_string)

        ), timeout=30)  # 30 seconds timeout
        print(bestbuy_price)
        print(walmart_price)
        print(newegg_price)
        return {
            "BestBuy": bestbuy_price,
            "Newegg": newegg_price,
            "Walmart": walmart_price
        }
    except TimeoutError:
        return HTTPException(status_code=408, detail="Request timeout, one or more scrapers did not finish in time.")
    except Exception as e:
        # Logging the error and returning a 500 server error response
        print(f"An error occurred: {str(e)}")
        return HTTPException(status_code=500, detail=str(e))

# Remove the test function and main execution block for production deployment
