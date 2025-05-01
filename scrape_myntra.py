from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re  # For regular expression to extract image URLs

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Function to scrape product data and save it to Firestore
def scrape_and_store_products_myntra(url, collection_name):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(5)  # wait for JS to render content fervre

    soup = BeautifulSoup(driver.page_source, "html.parser")
    products = soup.find_all("li", {"class": "product-base"})

    counter = 0
    for product in products:
        if counter >= 8:
            break

        brand_tag = product.find("h3", {"class": "product-brand"})
        brand = brand_tag.text.strip() if brand_tag else "No Brand"

        name_tag = product.find("h4", {"class": "product-product"})
        product_name = name_tag.text.strip() if name_tag else "No Product Name"

        price_tag = product.find("span", {"class": "product-discountedPrice"})
        price = price_tag.text.strip() if price_tag else "No Price"

        original_price_tag = product.find("span", {"class": "product-strike"})
        original_price = original_price_tag.text.strip() if original_price_tag else "No Original Price"

        discount_tag = product.find("span", {"class": "product-discountPercentage"})
        discount = discount_tag.text.strip() if discount_tag else "No Discount"

        product_link_tag = product.find("a", href=True)
        if product_link_tag:
            href = product_link_tag['href']
            if not href.startswith("/"):
                href = "/" + href
            link = "https://www.myntra.com" + href
        else:
            link = "No Link"

        # Visit the product page to collect all images
        driver.get(link)
        time.sleep(5)  # wait for the page to load

        # Scraping the product's detailed page for image URLs
        detailed_page_soup = BeautifulSoup(driver.page_source, "html.parser")
        image_divs = detailed_page_soup.find_all("div", {"class": "image-grid-image"})
        image_urls = []

        for div in image_divs:
            style = div.get('style', '')
            match = re.search(r'url\("([^"]+)"\)', style)
            if match:
                image_urls.append(match.group(1))

        # Print details in terminal
        print(f"Product {counter+1}:")
        print(f"  Brand: {brand}")
        print(f"  Name: {product_name}")
        print(f"  Price: {price}")
        print(f"  Original Price: {original_price}")
        print(f"  Discount: {discount}")
        print(f"  Image URLs: {image_urls}")
        print(f"  Link: {link}")
        print("-" * 80)

        # Uncomment this to save to Firestore
        db.collection(collection_name).add({
            "brand": brand,
            "product_name": product_name,
            "price": price,
            "original_price": original_price,
            "discount": discount,
            "image_urls": image_urls,  # Store multiple image URLs as a list
            "link": link
        })

        counter += 1

    driver.quit()
    print(f"Scraped data for {collection_name} pushed to Firestore.\n\n")


# Myntra URLs for different categories
pants_url = "https://www.myntra.com/men-pants"
tshirts_url = "https://www.myntra.com/men-tshirts"
casual_shirts_url = "https://www.myntra.com/men-casual-shirts"
formal_shirts_url = "https://www.myntra.com/men-formal-shirts"
jeans_url = "https://www.myntra.com/men-jeans"
track_pants_url = "https://www.myntra.com/men-track-pants"
shorts_url = "https://www.myntra.com/men-shorts"
trousers_url = "https://www.myntra.com/men-trousers"

# Scrape and store products for each category
scrape_and_store_products_myntra(pants_url, "pants")
scrape_and_store_products_myntra(tshirts_url, "tshirts")
scrape_and_store_products_myntra(casual_shirts_url, "casual_shirts")
scrape_and_store_products_myntra(formal_shirts_url, "formal_shirts")
scrape_and_store_products_myntra(jeans_url, "jeans")
scrape_and_store_products_myntra(track_pants_url, "track_pants")
scrape_and_store_products_myntra(shorts_url, "shorts")
scrape_and_store_products_myntra(trousers_url, "trousers")
