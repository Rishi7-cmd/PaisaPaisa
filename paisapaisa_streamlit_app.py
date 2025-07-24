import streamlit as st
import pandas as pd
import base64
import io
from openpyxl import Workbook
from openpyxl.styles import PatternFill

# ✨ Custom Diwali theme with spaced glow
st.markdown("""
    <style>
        html, body, [class*="css"] {
            background-color: #0e0e0e !important;
        }

        .title-box {
            text-align: center;
            line-height: 1.5;
            margin-top: 30px;
            margin-bottom: 0px;
        }

        .title-glow {
            font-size: 38px;
            font-weight: 900;
            color: #ffcc00;
            text-shadow:
                0 0 5px #ffcc00,
                0 0 10px #ff9900,
                0 0 15px #ff6600,
                0 0 20px #ff3300;
        }

        .subtext {
            text-align: center;
            font-size: 16px;
            color: #cccccc;
            margin-bottom: 40px;
        }

        .stFileUploader label {
            font-size: 18px;
            color: #dddddd;
        }

        .stButton>button {
            background-color: #ff9900;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Title section
st.markdown("""
    <div class="title-box">
        <div class="title-glow">🪔 PaisaPaisa Layered</div>
        <div class="title-glow">Transaction Flowchart</div>
    </div>
""", unsafe_allow_html=True)

# Subtitle
st.markdown('<div class="subtext">Upload a transaction Excel file and get a processed flowchart-style Excel as output.</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

def process_excel(file):
    df = pd.read_excel(file)

    df = df[df['Amount'] > 50000]

    wb = Workbook()
    ws = wb.active
    ws.title = "Flowchart"

    headers = ["Victim", "Layer 1", "Layer 2", "Withdrawal", "Amount"]
    ws.append(headers)

    for _, row in df.iterrows():
        l2 = row['Layer 2 Account'] if pd.notna(row['Layer 2 Account']) else ""
        withdrawal = row['Withdrawal']
        amt = row['Amount']
        out = [row['Victim Account'], row['Layer 1 Account'], l2, withdrawal, amt]
        ws.append(out)

        if amt > 100000:
            for col in range(1, 6):
                ws.cell(row=ws.max_row, column=col).fill = PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid")

    out_file = io.BytesIO()
    wb.save(out_file)
    return out_file.getvalue()

if uploaded_file:
    with st.spinner("Generating your Diwali-style flowchart..."):
        result_bytes = process_excel(uploaded_file)
        st.success("🎉 Done! Download your Excel below.")
        st.download_button("📥 Download Processed Excel", result_bytes, file_name="flowchart_output.xlsx")
