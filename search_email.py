import time
import urllib.parse

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

EXCEL_FILE = "speakers.xlsx"
SEARCH_ENGINE = "https://www.google.com/search?q="
PAGE_LOAD_TIMEOUT = 15  # seconds — raise if on a slow connection


def main():
    df = pd.read_excel(EXCEL_FILE)

    options = Options()
    # Suppress GCM/push-notification noise in the console
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-first-run")
    options.add_argument("--log-level=3")  # fatal only
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    # Cap how long driver.get() will wait for a page to load
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

    for i, row in df.iterrows():
        try:
            name = str(row["NAME"]).strip()
            affiliation = str(row["Affilation"]).strip()

            query = f"{name} {affiliation} email"
            url = SEARCH_ENGINE + urllib.parse.quote(query)

            driver.switch_to.new_window("tab")

            try:
                driver.get(url)
            except Exception as load_err:
                # Page load timed out — tab is still open and usable, keep going
                print(f"  ⚠ Page load timeout at row {i}, continuing: {load_err}")

            print(query)
            time.sleep(1)  # brief pause so tabs don't pile up instantly

        except Exception as e:
            print(f"Failed at row {i}: {e}")
            time.sleep(3)

    print("\nFinished opening all tabs.")
    input("Press ENTER to close the browser...")
    driver.quit()


if __name__ == "__main__":
    main()
