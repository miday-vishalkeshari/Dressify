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
def scrape_and_store_products_myntra(url):
    options = Options()
    options.headless = True
    options.add_argument("--log-level=3")  # Suppress warnings and errors
    driver = webdriver.Chrome(options=options)

    try:
        if url != "No Link":
            driver.get(url)
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

    finally:
        driver.quit()

# Function to read product links from CSV
def read_product_links_from_csv(file_path):
    df = pd.read_csv(file_path)
    if "ProductLink" not in df.columns:
        raise ValueError("The CSV file must contain a 'ProductLink' column.")
    return df["ProductLink"].tolist()

# Function to scrape and process products from CSV links
def scrape_products_from_csv(file_path):
    product_links = read_product_links_from_csv(file_path)
    for idx, url in enumerate(product_links):
        print(f"Scraping Product {idx + 1}: {url}")
        scrape_and_store_products_myntra(url)

# Run the scraping process
if __name__ == "__main__":
    file_path = "product_links.csv"  # Path to your CSV file containing product links
    scrape_products_from_csv(file_path)