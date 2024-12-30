# scraper.py - Orchestrates the scraping process using helpers

from bs4 import BeautifulSoup
import requests
import random
from .helpers import get_title, get_prices, get_image, get_rating, get_review_count, get_bsr, get_published_date
from .userAgents import user_agents
import re
import unicodedata

# Function to generate the url for the amazon search
def generate_amazon_search_url(search_query, type):
    import urllib.parse
    base_url = "https://www.amazon.com/s"
    types = {"newestArrivals": "date-desc-rank", "bestSellers": "exact-aware-popularity-rank"}

    params = {
        "k": search_query,                                      # Search query
        "s": types.get(type, "exact-aware-popularity-rank"),    # Sort by type of search
        "crid": "",                                             # Optional: category or filter ID
        # "qid": "1734455311",                                    # Timestamp for query ID
        "sprefix": f"{search_query[:10]}",                      # Prefix for search completion
        # "ref": "sr_st_date-desc-rank",                          # Sort rank reference
    }

    # Encode the query parameters into a URL
    query_string = urllib.parse.urlencode(params)

    return f"{base_url}?{query_string}"


# Function to generate header
def generate_header():
    return {
        "User-Agent": user_agents[random.randint(0, 999)],
        'Accept-Language': 'en-US, en;q=0.5', 
        "Referer": "https://www.amazon.com/", 
        "Accept-Encoding": "gzip, deflate, br"
    }


# Function to scrape amazon
def scrape_amazon_products(search_query, type="bestSellers"):

    URL = generate_amazon_search_url(search_query, type)
    webpage = requests.get(URL, headers=generate_header())
    soup = BeautifulSoup(webpage.content, "html.parser")

    print(URL)
    print(webpage.content)

    links = soup.find_all("a", attrs={'class': 'a-link-normal s-line-clamp-4 s-link-style a-text-normal'})
    links_list = [link.get('href') for link in links]

    # Keep only the first 20 links
    # links_list = links_list[:30]

    print(links_list)
    
    products = []
    for index, link in enumerate(links_list):
        full_url = "https://www.amazon.com" + link
        new_webpage = requests.get(full_url, headers=generate_header())
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        products.append({
            "link": full_url,
            "title": get_title(new_soup),
            "prices": ' - '.join(get_prices(new_soup)),
            "image": get_image(new_soup),
            "rating": get_rating(new_soup),
            "reviews": get_review_count(new_soup),
            "bsr": get_bsr(new_soup),
            "date": get_published_date(new_soup)
        })

        print(f"{index}th product completed")

    products = [product for product in products if product.get('title', '').strip() != '']
    return products