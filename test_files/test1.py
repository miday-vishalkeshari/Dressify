from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium WebDriver
driver = webdriver.Chrome()

# URL to test
url = "https://www.myntra.com/track-pants/bewakoof/bewakoof-men-track-pants/27407520/buy"

# Open the URL
driver.get(url)

try:
    # Wait for the parent div containing color options to load
    color_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mountRoot"]/div/div[1]/main/div[2]/div[2]/div[2]/div[1]/div'))
    )
    
    # Find all <a> tags within the div
    color_links = color_div.find_elements(By.TAG_NAME, "a")
    
    # Extract the title attribute from each <a> tag
    color_options = [link.get_attribute("title") for link in color_links if link.get_attribute("title")]

    # Print the extracted colors
    print("Available Colors:", color_options)

except Exception as e:
    print("Error:", e)

finally:
    # Close the WebDriver
    driver.quit()