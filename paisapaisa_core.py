
import io
import pandas as pd

def process_excel(uploaded_file):
    # Read Excel into a DataFrame
    df = pd.read_excel(uploaded_file)

    # Example transformation logic (replace with actual logic)
    df['Processed_Amount'] = df['Amount'] * 1.18  # GST example

    # Save output to in-memory buffer
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Processed')
    output.seek(0)
    return output
