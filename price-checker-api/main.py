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
        # Setting an overall timeout for all scraper tasks
        results = await wait_for(gather(
            scrape_bestbuy(decoded_string),
            scrape_newegg(decoded_string),
            scrape_walmart(decoded_string)
        ), timeout=30)  # 30 seconds timeout

        # Extracting prices and URLs from results
        bestbuy_price = results[0]["price"]
        bestbuy_url = results[0]["product_url"]
        print(bestbuy_url)
        newegg_price = results[1]["price"]
        newegg_url = results[1]["product_url"]
        print(newegg_url)
        walmart_price = results[2]["price"]
        walmart_url = results[2]["product_url"]
        print(walmart_url)
        

        return {
            "BestBuy": {"price": bestbuy_price, "product_url": bestbuy_url},
            "Newegg": {"price": newegg_price, "product_url": newegg_url},
            "Walmart": {"price": walmart_price, "product_url": walmart_url}
        }
    except TimeoutError:
        return HTTPException(status_code=408, detail="Request timeout, one or more scrapers did not finish in time.")
    except Exception as e:
        # Logging the error and returning a 500 server error response
        print(f"An error occurred: {str(e)}")
        return HTTPException(status_code=500, detail=str(e))
