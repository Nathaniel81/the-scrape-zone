import pandas as pd

# Load the Excel file
file_path = "tst.xlsx"
sheet_name = "Sheet1"
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Clean the Name column
df['NAME'] = df['NAME'].str.strip()

# Clean the Email column
df['EMAIL'] = df['EMAIL'].str.strip()
df['EMAIL'] = df['EMAIL'].str.lower()
df['EMAIL'] = df['EMAIL'].str.rstrip('.')

# Save the cleaned data back to Excel
output_path = "International conference on biotechnology Jun 22, 2025.xlsx"
df.to_excel(output_path, index=False)

print(f"Cleaned data has been saved to {output_path}")
