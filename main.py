from fastapi import FastAPI
from scraper_bestbuy import scrape_bestbuy
from scraper_newegg import scrape_newegg
from scraper_walmart import scrape_walmart

app = FastAPI()

@app.get("/prices/")
async def get_prices(product_name: str):
    bestbuy_price = scrape_bestbuy(product_name)
    newegg_price = scrape_newegg(product_name)
    walmart_price = scrape_walmart(product_name)
    return {
        "BestBuy": bestbuy_price,
        "Newegg": newegg_price,
        "Walmart": walmart_price
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
