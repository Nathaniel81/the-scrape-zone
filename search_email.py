import time
import urllib.parse

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


EXCEL_FILE = "speakers.xlsx"

SEARCH_ENGINE = "https://www.google.com/search?q="

DELAY = 1  # seconds between opening tabs


def main():

    df = pd.read_excel(EXCEL_FILE)

    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        ),
        options=options
    )

    first = True

    for _, row in df.iterrows():

        name = str(row["NAME"]).strip()
        affiliation = str(row["Affilation"]).strip()

        query = f"{name} {affiliation} email"

        url = SEARCH_ENGINE + urllib.parse.quote(query)

        if first:
            driver.get(url)
            first = False
        else:
            driver.switch_to.new_window("tab")
            driver.get(url)

        print(query)

        time.sleep(DELAY)

    print("\nFinished opening all tabs.")
    input("Press ENTER to close the browser...")

    driver.quit()


if __name__ == "__main__":
    main()