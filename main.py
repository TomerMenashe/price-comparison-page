from scraper_bestbuy import search_and_get_bestbuy_price
from scraper_walmart import search_and_get_walmart_price
from scraper_newegg import search_and_get_newegg_price

def main():
    product_name = input("Enter the product name: ")

    price_bb = search_and_get_bestbuy_price(product_name)
    price_wm = search_and_get_walmart_price(product_name)
    price_ne = search_and_get_newegg_price(product_name)

    print(f"Price at Best Buy: {price_bb}")
    print(f"Price at Walmart: {price_wm}")
    print(f"Price at Newegg: {price_ne}")

if __name__ == "__main__":
    main()
