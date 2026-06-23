import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# Selenium function to fetch names and affiliations dynamically
def fetch_speaker_data_with_selenium(url, wait_class, speaker_class, name_selector, affiliation_selector):
    # options = webdriver.ChromeOptions()
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # # options = Options()
    # service = Service(executable_path='chromedriver.exe')
    # driver = webdriver.Chrome(service=service, options=options)
    # driver.get(url)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, wait_class)))
    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        return []

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    speakers_section = soup.find_all('div', class_=speaker_class)
    speaker_data = []

    for speaker in speakers_section:
        name_element = speaker.select_one(name_selector)
        affiliation_element = speaker.select_one(affiliation_selector)
        if name_element and affiliation_element:
            speaker_data.append((name_element.get_text(strip=True), affiliation_element.get_text(strip=True)))

    driver.quit()
    return speaker_data

# Function to open Google search tabs
def open_search_tabs(speaker_data):
    options = Options()
    # Not headless because we need to *see* the tabs
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)

    for name, affiliation in speaker_data:
        search_query = f"{name} {affiliation} email"
        url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        driver.execute_script(f"window.open('{url}', '_blank');")
        time.sleep(1)  # slight delay to prevent overloading the browser

    print("✅ All search tabs opened. Go check them manually!")
    # Keep the browser open
    input("Press Enter to close the browser after you're done...")
    driver.quit()

# Main script
def main():
    # Get user inputs for dynamic selectors
    url = input("Enter the URL of the webpage: ")
    wait_class = input("Enter the class name for WebDriverWait (CSS selector): ")
    speaker_class = input("Enter the speaker section class (CSS selector): ")
    name_selector = input("Enter the CSS selector for the name element: ")
    affiliation_selector = input("Enter the CSS selector for the affiliation element: ")

    speakers = fetch_speaker_data_with_selenium(url, wait_class, speaker_class, name_selector, affiliation_selector)

    if speakers:
        open_search_tabs(speakers)
    else:
        print("No speakers found.")

if __name__ == "__main__":
    main()
