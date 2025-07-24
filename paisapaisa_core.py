import pandas as pd
import re

def process_excel(file):
    df = pd.read_excel(file)

    # Try to find the 'Amount' column flexibly
    amount_col = None
    for col in df.columns:
        if re.search(r'amount', col, re.IGNORECASE):
            amount_col = col
            break

    if not amount_col:
        raise KeyError("Could not find any column containing 'amount' in its name. Please check your Excel.")

    # GST example (can remove this if not needed)
    df['Processed_Amount'] = df[amount_col] * 1.18

    # Add any additional processing here if needed
    return df
