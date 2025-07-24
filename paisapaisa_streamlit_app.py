
import streamlit as st
import pandas as pd
import io

# Set page config with emoji and title
st.set_page_config(page_title="PaisaPaisa Flowchart Generator", page_icon="🪔", layout="centered")

# Inject custom Diwali-styled background
diwali_css = '''
<style>
body {
    background-image: url("https://images.unsplash.com/photo-1604081443663-3af7a8204f5b");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
    color: #f5f5f5;
}
section.main > div {
    background-color: rgba(0, 0, 0, 0.75);
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 0 20px #ffcc00;
}
h1, h2, h3, h4, h5, h6 {
    color: #ffe066 !important;
}
</style>
'''
st.markdown(diwali_css, unsafe_allow_html=True)

# App title
st.title("🪔 PaisaPaisa Layered Transaction Flowchart")
st.markdown("Upload a transaction Excel file and get a processed flowchart-style Excel as output.")

# Core processing logic
def process_excel(file, base_filename):
    df = pd.read_excel(file)

    # Example transformation: (customize as needed)
    df['Layer'] = df['Layer'].fillna(method='ffill')
    df = df[df['Amount'] > 50000]  # Filter: amount over 50K
    df = df[df['Layer'] <= 2]      # Filter: up to Layer 2
    df = df[df['Withdrawal'] > 0]  # Filter: withdrawals only

    # Highlight large withdrawals
    df['Flag'] = df['Withdrawal'].apply(lambda x: "🚨" if x > 100000 else "")

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Filtered')
        workbook  = writer.book
        worksheet = writer.sheets['Filtered']
        format_red = workbook.add_format({'font_color': 'red', 'bold': True})
        worksheet.conditional_format('G2:G1000', {'type': 'text',
                                                  'criteria': 'containing',
                                                  'value': '🚨',
                                                  'format': format_red})
    output.seek(0)
    return output

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    base_filename = uploaded_file.name.rsplit(".", 1)[0]
    output_buffer = process_excel(uploaded_file, base_filename)
    st.success("✅ Processing complete!")
    st.download_button(
        label="📥 Download Result Excel",
        data=output_buffer,
        file_name=f"{base_filename}_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
