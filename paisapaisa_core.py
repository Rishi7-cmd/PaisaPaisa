import pandas as pd

def process_excel(uploaded_file):
    df = pd.read_excel(uploaded_file)

    # Try to find the correct column name for Amount
    amount_col = None
    for col in df.columns:
        if "amount" in col.lower():
            amount_col = col
            break

    if amount_col is None:
        raise KeyError("No amount column found in the Excel file.")

    # Clean the amount column: remove commas, extract numbers, convert to float
    df[amount_col] = (
        df[amount_col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.extract(r"([\d.]+)")[0]
        .astype(float)
    )

    # Example: Create a processed column using GST multiplier
    df["Processed_Amount"] = df[amount_col] * 1.18  # Adjust multiplier as needed

    # You can return or further process the dataframe here
    return df
