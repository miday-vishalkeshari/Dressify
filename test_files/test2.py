import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv

# Function to scrape product data
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

            print(f"Product scraped successfully: {product_name}")
        else:
            print("No Link provided.")

    finally:
        driver.quit()

# Function to read product links from a CSV file
def read_product_links_from_csv(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        return [row[0] for row in reader]

# Function to fetch all color variant links for a product
def fetch_color_variant_links(product_url):
    options = Options()
    options.headless = True
    options.add_argument("--log-level=3")  # Suppress warnings and errors
    driver = webdriver.Chrome(options=options)

    driver.get(product_url)
    time.sleep(5)  # Wait for the page to load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    color_links = []

    # Find all <a> tags with the class "colors-image" inside them
    color_elements = soup.find_all("a", href=True, attrs={"data-refreshpage": "true"})
    for element in color_elements:
        href = element["href"]
        # Filter links to include only valid product links
        if href.startswith("/lounge-tshirts/u.s.+polo+assn."):  # Ensure the link belongs to the same brand
            full_link = "https://www.myntra.com" + href
            color_links.append(full_link)

    driver.quit()
    return color_links

# Function to process product links and fetch color variants
def process_product_links(file_path):
    product_links = read_product_links_from_csv(file_path)
    for idx, product_url in enumerate(product_links):
        print(f"Fetching color variants for Product {idx + 1}: {product_url}")
        color_links = fetch_color_variant_links(product_url)
        print("Color Variant Links:")
        for link in color_links:
            print(link)
        print("-" * 80)

# Function to scrape and process products from CSV links
def scrape_products_from_csv(file_path):
    product_links = read_product_links_from_csv(file_path)
    for idx, url in enumerate(product_links):
        print(f"Scraping Product {idx + 1}: {url}")
        scrape_and_store_products_myntra(url)

# Run the program
if __name__ == "__main__":
    file_path = "product_links.csv"  # Path to your CSV file containing product links
    process_product_links(file_path)
    scrape_products_from_csv(file_path)