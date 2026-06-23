import pandas as pd
from datetime import datetime

def save_excel(records):

    if not records:
        print("No data to save")
        return

    df = pd.DataFrame(records)

    filename = f"speakers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    df.to_excel(filename, index=False)

    print(f"Saved {len(df)} rows to {filename}")
