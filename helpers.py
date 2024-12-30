# helpers.py - Contains reusable scraping helper functions

from bs4 import BeautifulSoup
import re
import unicodedata

# Function to extract Product Title
def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Product Price
def get_prices(soup):
    try:
        centerColumn = soup.find("div", id="centerCol")
        price_div = centerColumn.find("div", id="corePrice_desktop")

        # Find all the price containers
        price_spans = price_div.find_all("span", class_="a-price")

        # Extract prices from the spans with the "a-offscreen" class
        prices = [span.find("span", class_="a-offscreen").text.strip() for span in price_spans if span.find("span", class_="a-offscreen")]

    except AttributeError:
        prices = []

    return prices

def get_image(soup):
    try:
        # Find the <img> tag
        img_tag = soup.find("img", id="landingImage")  # Find based on id or other attributes

        img_src = img_tag.get("src")
    
    except AttributeError:
        img_src = ""
    
    return img_src

# Function to extract Product Rating
def get_rating(soup):

    try:
        rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
    
    except AttributeError:
        rating = ""	

    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""	

    return review_count

# Function to extract the Best Seller Rating text
def get_bsr(soup):
    # Find all elements with class "a-list-item"
    list_items = soup.find_all("span", class_="a-list-item")

    # Search for the one that contains "Best Sellers Rank:"
    bsr_element = None
    for item in list_items:
        if "Best Sellers Rank:" in item.text:
            bsr_element = item
            break

    # Extract text while excluding links
    bsr_text = ""
    
    if bsr_element:
        bsr_text = ''.join(bsr_element.find_all(string=True)).strip()

        # Remove "Best Sellers Rank:" text
        bsr_text = re.sub(r"Best Sellers Rank:\s*", "", bsr_text)

    return bsr_text

# Function to extract the Published Date text
def get_published_date(soup):
    # Find all elements with class "a-list-item"
    list_items = soup.find_all("span", class_="a-list-item")

    # Search for the one that contains "Best Sellers Rank:"
    date_element = None
    for item in list_items:
        if "Date First Available" in item.text:
            date_element = item
            break

    # Extract text while excluding links
    date_text = ""
    
    if date_element:
        date_text = ''.join(date_element.find_all(string=True)).strip()

        # Extract the date from the "date" key
        date = re.search(r"Date First Available.*:\s*(.+)", date_text, re.DOTALL)
        
        if date:
            raw_date = date.group(1).strip()

            # Normalize the string to remove hidden Unicode characters
            normalized_date = unicodedata.normalize("NFKD", raw_date)

            # Clean up extraneous whitespace and Unicode characters
            cleaned_date = re.sub(r"\s+", " ", normalized_date)  # Replace multiple spaces/newlines with a single space
            # Remove the specific invisible character
            cleaned_date = cleaned_date.replace("\u200e", "").strip()
            cleaned_date = cleaned_date.strip()          # Remove leading/trailing spaces
            date_text = cleaned_date

    return date_text
