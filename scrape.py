import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# Function to search emails using SerpAPI
def search_emails_with_serpapi(name, affiliation, api_key):
    query = f"{name} {affiliation} email"
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        results = response.json()
        email_candidates = []
        for result in results.get("organic_results", []):
            snippet = result.get("snippet", "")
            # Extract potential email patterns
            emails = [word for word in snippet.split() if "@" in word]
            email_candidates.extend(emails)
        
        return email_candidates
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

# Selenium function to fetch names and affiliations dynamically
def fetch_speaker_data_with_selenium(url, wait_class, speaker_class, name_selector, affiliation_selector):
    options = Options()
    options.headless = True
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    # Wait for the specific section to load
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, wait_class)))
    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        return []

    # Get the page source and parse
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract speaker data
    speakers_section = soup.find_all('div', class_=speaker_class)
    speaker_data = []

    for speaker in speakers_section:
        name_element = speaker.select_one(name_selector)
        affiliation_element = speaker.select_one(affiliation_selector)
        if name_element and affiliation_element:
            speaker_data.append((name_element.get_text(strip=True), affiliation_element.get_text(strip=True)))

    driver.quit()
    return speaker_data

# Main script
def main():
    serpapi_key = os.getenv('SERPAPI_KEY')

    # Get user inputs for dynamic selectors
    url = input("Enter the URL of the webpage: ")
    wait_class = input("Enter the class name for WebDriverWait (CSS selector): ")
    speaker_class = input("Enter the speaker section class (CSS selector): ")
    name_selector = input("Enter the CSS selector for the name element: ")
    affiliation_selector = input("Enter the CSS selector for the affiliation element: ")

    # Fetch speaker data
    speakers = fetch_speaker_data_with_selenium(url, wait_class, speaker_class, name_selector, affiliation_selector)

    if speakers:
        for name, affiliation in speakers:
            print(f"Searching email for {name}, {affiliation}...")
            emails = search_emails_with_serpapi(name, affiliation, serpapi_key)
            if emails:
                print(f"Found emails: {emails}")
            else:
                print("No emails found.")
    else:
        print("No speakers found.")

if __name__ == "__main__":
    main()
