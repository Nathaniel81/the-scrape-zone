import requests
from bs4 import BeautifulSoup


def search_person(name, affiliation):

    query = f"{name} {affiliation}"

    url = "https://html.duckduckgo.com/html/"

    response = requests.post(
        url,
        data={"q": query},
        timeout=20
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    results = []

    for a in soup.select("a.result__a")[:5]:

        href = a.get("href")

        if href:
            results.append(href)

    return results
