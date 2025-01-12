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

# Selenium function to fetch names and affiliations
def fetch_speaker_data_with_selenium(url):
    options = Options()
    options.headless = True
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.speakers-mircim')))
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    speakers_section = soup.find_all('div', class_='speakers-item')
    speaker_data = []

    for speaker in speakers_section:
        name = speaker.find('h2')
        affiliation = speaker.find('span')
        if name and affiliation:
            speaker_data.append((name.get_text(strip=True), affiliation.get_text(strip=True)))

    driver.quit()
    return speaker_data

# Main script
def main():
    serpapi_key = os.getenv('SERPAPI_KEY')
    url = "https://empendium.com/mircim/speakers"
    speakers = fetch_speaker_data_with_selenium(url)

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
