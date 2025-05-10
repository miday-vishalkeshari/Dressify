from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Function to scrape product data and save it to Firestore
def scrape_and_store_products_myntra(url, collection_name):
    options = Options()
    options.headless = True
    options.add_argument("--log-level=3")  # Suppress warnings and errors
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(5)  # wait for JS to render content

    soup = BeautifulSoup(driver.page_source, "html.parser")
    products = soup.find_all("li", {"class": "product-base"})

    counter = 0
    for product in products:
        if counter >= 2:
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

        # Navigate to the product link to fetch all image URLs dynamically
        if link != "No Link":
            driver.get(link)
            time.sleep(3)  # Wait for the product page to load
            product_soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Find all divs with class "image-grid-image" inside "image-grid-col50"
            parent_divs = product_soup.find_all("div", {"class": "image-grid-col50"})
            image_urls = []
            
            for parent_div in parent_divs:
                child_divs = parent_div.find_all("div", {"class": "image-grid-image"})
                for child_div in child_divs:
                    if "style" in child_div.attrs:  # Extract URLs from style attribute
                        style_attr = child_div["style"]
                        start = style_attr.find("url(") + 4
                        end = style_attr.find(")", start)
                        image_url = style_attr[start:end].strip('"').strip("'")
                        image_urls.append(image_url)
        else:
            image_urls = []

        # Print only the image URLs
        print(f"Image URLs: {image_urls}")

        # Print details in terminal
        print(f"Product {counter+1}:")
        print(f"  Brand: {brand}")
        print(f"  Name: {product_name}")
        print(f"  Price: {price}")
        print(f"  Original Price: {original_price}")
        print(f"  Discount: {discount}")
        print(f"  Link: {link}")
        print("-" * 80)

        counter += 1

    driver.quit()
    print(f"Scraped data for {collection_name} pushed to Firestore.\n\n")


# Myntra URLs for different categories
pants_url = "https://www.myntra.com/men-pants"

# Scrape and store products for each category
scrape_and_store_products_myntra(pants_url, "pants")