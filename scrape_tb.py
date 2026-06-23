import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

headers = {"User-Agent": "Mozilla/5.0"}

def get_bing_links(query):
    url = f"https://www.bing.com/search?q={query}"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    links = []
    for h2 in soup.find_all("h2"):
        a = h2.find("a")
        if a and a["href"].startswith("http"):
            links.append(a["href"])
    return links[:3]  # limit to top 3 results for speed

def extract_emails_from_url(url):
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return []
        return re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", res.text)
    except:
        return []

# Load your Excel file
df = pd.read_excel("lecturers.xlsx")
results = []

for index, row in df.iterrows():
    NAME = row['NAME']
    Affilation = row['Affilation']
    query = f"{NAME} {Affilation} email"
    print(f"\nSearching for: {query}")
    emails = set()

    links = get_bing_links(query)
    print(f"Found {len(links)} links")

    for link in links:
        found = extract_emails_from_url(link)
        emails.update(found)
        time.sleep(2)  # delay between requests

    results.append({
        "NAME": NAME,
        "Affilation": Affilation,
        "emails": list(emails)
    })

    time.sleep(3)  # delay between Bing searches

# Save to Excel
emails_df = pd.DataFrame(results)
emails_df.to_excel("results_with_emails.xlsx", index=False)
print("Done.")
