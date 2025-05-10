import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# URLs for pants and shirts (you can modify these to target the respective categories)
pants_url = "https://www.amazon.in/s?k=pants+for+men"

# Headers for web scraping
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

# Function to scrape product data and save it to Firestore
def scrape_and_store_products(url, collection_name):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find product containers
    products = soup.find_all("div", {"data-component-type": "s-search-result"})

    # Limit to 10 products for testing
    counter = 0
    for product in products:
        if counter >= 10:  # Break the loop after 10 products
            break

        # Extract product details (title, link, image)
        h2_tag = product.find("h2")
        title = h2_tag.text.strip() if h2_tag else product.find("img")['alt'] if product.find("img") else "No Title"

        a_tag = product.find("a", href=True)
        link = "https://www.amazon.in" + a_tag['href'] if a_tag else "No Link"

        img_tag = product.find("img")
        image_url = img_tag['src'] if img_tag else "No Image"

        # Store the product data in Firestore under the specified collection
        db.collection(collection_name).add({
            "title": title,
            "link": link,
            "image_url": image_url
        })

        counter += 1

    print(f"Scraped data for {collection_name} pushed to Firestore.")

# Scrape and store data for pants
scrape_and_store_products(pants_url, "pants")

# Scrape and store data for shirts (you can reuse this function for shirts too)
shirts_url = "https://www.amazon.in/s?k=shirts+for+men"
scrape_and_store_products(shirts_url, "shirts")

