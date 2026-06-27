import time
import urllib.parse

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

EXCEL_FILE = "speakers.xlsx"
SEARCH_ENGINE = "https://www.google.com/search?q="
PAGE_LOAD_TIMEOUT = 15


def get_active_window(driver):
    """Return a live window handle, opening a blank tab if none exist."""
    handles = driver.window_handles
    if handles:
        driver.switch_to.window(handles[-1])
        return True
    # All tabs were closed — open a new blank one to revive the session
    driver.execute_script("window.open('about:blank', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    return True


def open_tabs(driver, df, j):
    for i, row in df.iterrows():
        try:
            name = str(row.get("NAME", "")).strip()
            affiliation = str(row.get("Affilation", "")).strip()

            if not name or name.lower() == "nan":
                print(f"  ⚠ Skipping row {i}: missing NAME")
                continue
            if not affiliation or affiliation.lower() == "nan":
                print(f"  ⚠ Skipping row {i}: missing Affilation")
                continue

            query = f"{name} {affiliation} email"
            url = SEARCH_ENGINE + urllib.parse.quote(query)

            get_active_window(driver)
            driver.switch_to.new_window("tab")

            try:
                driver.get(url)
            except Exception as load_err:
                print(f"  ⚠ Page load timeout at row {i}, continuing: {load_err}")

            print(query)

            if j == 0:
                print("  ⏳ Waiting 60s for first tab...")
                time.sleep(60)

            j += 1
            time.sleep(1)

        except Exception as e:
            print(f"Failed at row {i}: {e}")
            time.sleep(3)

    return j

def main():
    options = Options()
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-first-run")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

    j = 0
    while True:
        df = pd.read_excel(EXCEL_FILE)
        print(f"\nLoaded {len(df)} rows from {EXCEL_FILE}.")
        print(f"Columns found: {list(df.columns)}\n")  # helps catch column name typos
        print("Opening tabs...\n")

        j = open_tabs(driver, df, j)

        print("\nFinished opening all tabs.")
        print("  [C] Continue — update the Excel file, then press C to load the next batch")
        print("  [Q] Quit    — close the browser and exit")

        while True:
            choice = input("\nYour choice (C / Q): ").strip().upper()
            if choice == "C":
                input("  Update your Excel file now, then press ENTER to continue...")
                break
            elif choice == "Q":
                print("Closing browser...")
                driver.quit()
                return
            else:
                print("  Please type C to continue or Q to quit.")


if __name__ == "__main__":
    main()
