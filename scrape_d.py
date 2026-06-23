from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time

# === Setup Selenium Driver ===
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Optional: run in background
driver = webdriver.Chrome(service=Service(), options=options)

# === User Inputs ===
url = input("Enter the URL of the speaker list page: ").strip()
mode = input("Use CSS selectors? (yes/no): ").strip().lower()

data = []

# === Load Page ===
driver.get(url)
time.sleep(5)  # Wait for JS to load

if mode == "yes":
    # CSS Selectors provided
    name_selector = input("Enter the CSS selector for speaker names: ").strip()
    affiliation_selector = input("Enter the CSS selector for affiliations: ").strip()

    names = driver.find_elements(By.CSS_SELECTOR, name_selector)
    affiliations = driver.find_elements(By.CSS_SELECTOR, affiliation_selector)

    for i in range(min(len(names), len(affiliations))):
        name = names[i].text.strip()
        affiliation = affiliations[i].text.strip()
        data.append({"Name": name, "Affiliation": affiliation})

else:
    # Fallback method: loop over <div> blocks looking for <p> structure
    containers = driver.find_elements(By.TAG_NAME, "div")
    for container in containers:
        ps = container.find_elements(By.TAG_NAME, "p")
        if len(ps) >= 2:
            name = ps[0].text.strip()
            affiliation = ps[1].text.strip()
            if name and affiliation:
                data.append({"Name": name, "Affiliation": affiliation})

# === Export to Excel ===
df = pd.DataFrame(data)
output_file = "speakers_list.xlsx"
df.to_excel(output_file, index=False)

print(f"\n✅ Done! Data saved to {output_file}")

driver.quit()
