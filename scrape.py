from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests

# Function to check and fetch speaker data using requests
def fetch_speaker_data_with_requests(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the speaker section
    speakers_section = soup.find_all('div', class_='speaker')

    if not speakers_section:
        return None  # Return None if no data is found (likely JavaScript-loaded content)
    
    # Extract speaker data if found
    speaker_names = []
    affiliations = []
    for speaker in speakers_section:
        name = speaker.find('h3').get_text(strip=True)
        affiliation = speaker.find('p', class_='affiliation').get_text(strip=True)
        
        speaker_names.append(name)
        affiliations.append(affiliation)

    return list(zip(speaker_names, affiliations))

# Function to fetch speaker data with Selenium (for JavaScript-rendered content)
def fetch_speaker_data_with_selenium(url):
    # Setup Selenium WebDriver
    options = Options()
    options.headless = True  # Run browser in headless mode (without GUI)
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(url)

    # Wait for the speaker section to load
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.wp-block-media-text__content')))  # Modify selector if needed
    except TimeoutException:
        print("Timeout while waiting for the speaker section to load.")
        driver.quit()
        return None

    # Get the page source after JavaScript has rendered the content
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract speaker data
    speakers_section = soup.find_all('div', class_='wp-block-media-text__content')  # Modify based on actual page structure

    speaker_names = []
    affiliations = []
    for speaker in speakers_section:
        name = speaker.find('h4')
        if name:
            speaker_names.append(name.get_text(strip=True))
        else:
            speaker_names.append("No name found")

        # affiliation = speaker.find('p', class_='wp-block-uagb-faq')
        affiliation = soup.find('p')
        if affiliation:
            affiliations.append(affiliation.get_text(strip=True))
        else:
            affiliations.append("No affiliation found")

    driver.quit()  # Close the browser window

    return list(zip(speaker_names, affiliations))

# Main function to handle both static and dynamic loading
def get_speaker_data(url):
    # Try to fetch data using requests first (static content)
    speaker_data = fetch_speaker_data_with_requests(url)
    
    if speaker_data:
        print("Data fetched using requests:")
        return speaker_data  # If data is found, return it
    
    # If no data is found, try using Selenium (for dynamic content)
    print("Fetching data using Selenium (JavaScript-rendered content)...")
    return fetch_speaker_data_with_selenium(url)

url = 'https://web.natur.cuni.cz/cellbiol/phdconferenceimmuno/key-note-speakers/'
speaker_data = get_speaker_data(url)

# Print the fetched speaker data
if speaker_data:
    for speaker in speaker_data:
        print(f"Speaker: {speaker[0]}, Affiliation: {speaker[1]}")
else:
    print("No speaker data found.")
