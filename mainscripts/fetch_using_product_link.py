import pandas as pd
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

# Function to scrape product data and store it into Firestore
def scrape_and_store_products_myntra(url, collection_path):
    options = Options()
    options.headless = True
    options.add_argument("--log-level=3")  # Suppress warnings and errors
    driver = webdriver.Chrome(options=options)

    try:
        if url != "No Link":
            driver.get(url)
            time.sleep(3)  # Wait for the product page to load
            product_soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Extract product details
            try:
                brand = product_soup.find("h1", {"class": "pdp-title"}).text.strip()
            except AttributeError:
                brand = "N/A"

            try:
                product_name = product_soup.find("h1", {"class": "pdp-name"}).text.strip()
            except AttributeError:
                product_name = "N/A"

            try:
                price = product_soup.find("span", {"class": "pdp-price"}).text.strip()
            except AttributeError:
                price = "N/A"

            try:
                original_price = product_soup.find("span", {"class": "pdp-mrp"}).text.strip()
            except AttributeError:
                original_price = "N/A"

            try:
                discount = product_soup.find("span", {"class": "pdp-discount"}).text.strip()
            except AttributeError:
                discount = "N/A"

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

            # Prepare data to store in Firestore
            product_data = {
                "brand": brand,
                "product_name": product_name,
                "price": price,
                "original_price": original_price,
                "discount": discount,
                "image_urls": image_urls,
                "link": url
            }

            # Store data in Firestore
            doc_ref = db.collection(collection_path).document()
            doc_ref.set(product_data)

            print(f"Product stored successfully in Firestore: {product_name}")
        else:
            print("No Link provided.")

    finally:
        driver.quit()

# Function to read product links from CSV
def read_product_links_from_csv(file_path):
    df = pd.read_csv(file_path)
    if "ProductLink" not in df.columns:
        raise ValueError("The CSV file must contain a 'ProductLink' column.")
    return df["ProductLink"].tolist()

# Function to scrape and process products from CSV links
def scrape_products_from_csv(file_path, collection_path):
    product_links = read_product_links_from_csv(file_path)
    for idx, url in enumerate(product_links):
        print(f"Scraping Product {idx + 1}: {url}")
        scrape_and_store_products_myntra(url, collection_path)

# Run the scraping process
if __name__ == "__main__":
    file_path = "product_links_white_mentshirts.csv"  # Path to your CSV file containing product links
    collection_path = "Dressify_styles/tshirts/white"  # Firestore collection path
    scrape_products_from_csv(file_path, collection_path)