from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Function to scrape product links and save them to a CSV file
def scrape_and_store_products_myntra(url, collection_name, output_csv):
    options = Options()
    options.headless = True
    options.add_argument("--log-level=3")  # Suppress warnings and errors
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(5)  # wait for JS to render content

    soup = BeautifulSoup(driver.page_source, "html.parser")
    products = soup.find_all("li", {"class": "product-base"})

    product_links = []
    counter = 0
    for product in products:
        if counter >= 10:  # Limit to 2 products for testing
            break

        product_link_tag = product.find("a", href=True)
        if product_link_tag:
            href = product_link_tag['href']
            if not href.startswith("/"):
                href = "/" + href
            link = "https://www.myntra.com" + href
        else:
            link = "No Link"

        # Print details in terminal
        print(f"  Link: {link}")
        print("-" * 80)

        product_links.append(link)
        counter += 1

    driver.quit()

    # Write product links to a CSV file
    with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ProductLink"])  # Write header
        for link in product_links:
            writer.writerow([link])

    print(f"Scraped data for {collection_name} saved to {output_csv}.\n\n")

# Myntra URLs for different categories
style_url = "https://www.myntra.com/men-tshirts"

# Scrape and store products for each category
scrape_and_store_products_myntra(style_url, "men-tshirts", "product_links_raw.csv")





# # Myntra URLs for different categories
# pants_url = "https://www.myntra.com/men-pants"
# tshirts_url = "https://www.myntra.com/men-tshirts"
# casual_shirts_url = "https://www.myntra.com/men-casual-shirts"
# formal_shirts_url = "https://www.myntra.com/men-formal-shirts"
# jeans_url = "https://www.myntra.com/men-jeans"
# track_pants_url = "https://www.myntra.com/men-track-pants"
# shorts_url = "https://www.myntra.com/men-shorts"
# trousers_url = "https://www.myntra.com/men-trousers"

# # Scrape and store products for each category
# scrape_and_store_products_myntra(pants_url, "pants")
# # scrape_and_store_products_myntra(tshirts_url, "tshirts")
# # scrape_and_store_products_myntra(casual_shirts_url, "casual_shirts")
# # scrape_and_store_products_myntra(formal_shirts_url, "formal_shirts")
# # scrape_and_store_products_myntra(jeans_url, "jeans")
# # scrape_and_store_products_myntra(track_pants_url, "track_pants")
# # scrape_and_store_products_myntra(shorts_url, "shorts")
# # scrape_and_store_products_myntra(trousers_url, "trousers")