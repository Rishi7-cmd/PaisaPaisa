import streamlit as st
import pandas as pd
import io
import xlsxwriter

# Set page config
st.set_page_config(page_title="PaisaPaisa Layered Flowchart", layout="wide")

# Diwali-lit background CSS
st.markdown("""
    <style>
    body {
        background-color: #0d0d0d;
        background-image: radial-gradient(circle at 20% 30%, #ffcc00 0%, transparent 40%),
                          radial-gradient(circle at 80% 20%, #ff6600 0%, transparent 40%),
                          radial-gradient(circle at 50% 70%, #ff3399 0%, transparent 40%);
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #ffffff;
    }
    .css-1d391kg {background-color: rgba(0, 0, 0, 0.6);}
    .css-1offfwp {background-color: rgba(0, 0, 0, 0.6);}
    </style>
""", unsafe_allow_html=True)

st.title("🫤 PaisaPaisa Layered Transaction Flowchart")
st.write("Upload a transaction Excel file and get a processed flowchart-style Excel as output.")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

def process_excel(file, base_filename):
    df = pd.read_excel(file)

    # Rename if necessary
    if 'Disputed Amount' in df.columns:
        df.rename(columns={'Disputed Amount': 'Amount'}, inplace=True)

    if 'Amount' not in df.columns or 'Layer' not in df.columns or 'Withdrawal' not in df.columns:
        raise KeyError("Missing one of the required columns: Amount, Layer, Withdrawal")

    df_filtered = df[(df['Amount'] > 50000) & (df['Layer'] <= 2)]
    df_filtered = df_filtered[df_filtered['Withdrawal'].notnull()]

    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df_filtered.to_excel(writer, index=False, sheet_name='Filtered')

    workbook = writer.book
    worksheet = writer.sheets['Filtered']

    # Format for withdrawals over 1 lakh
    highlight_format = workbook.add_format({'bg_color': '#FF6666'})
    for row_num, amount in enumerate(df_filtered['Withdrawal'], start=1):
        if amount > 100000:
            worksheet.set_row(row_num, cell_format=highlight_format)

    writer.close()
    output.seek(0)

    return output

if uploaded_file is not None:
    filename = uploaded_file.name.rsplit('.', 1)[0]
    try:
        output_buffer = process_excel(uploaded_file, filename)
        st.success("\u2705 File processed successfully!")
        st.download_button(
            label="\ud83d\udcc5 Download Output Excel",
            data=output_buffer,
            file_name=f"{filename}_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"\u274c Failed to process file: {e}")
