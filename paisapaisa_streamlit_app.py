import streamlit as st
import pandas as pd
from paisapaisa_core import process_excel  # Your core logic

st.set_page_config(page_title="PaisaPaisa Flowchart", layout="centered")

# Diwali-themed background CSS
st.markdown("""
    <style>
        body {
            background-color: #0d0d0d;
            background-image:
              radial-gradient(circle at 10% 20%, rgba(255, 102, 0, 0.3) 2px, transparent 2px),
              radial-gradient(circle at 90% 30%, rgba(255, 255, 102, 0.2) 1px, transparent 2px),
              radial-gradient(circle at 50% 90%, rgba(255, 105, 180, 0.15) 2px, transparent 1px),
              radial-gradient(circle at 30% 70%, rgba(255, 140, 0, 0.25) 1.5px, transparent 1px);
            background-size: 30px 30px;
            animation: diwaliGlow 3s ease-in-out infinite alternate;
        }

        @keyframes diwaliGlow {
            from {
                background-position: 0 0, 10px 10px, 20px 20px, 30px 30px;
            }
            to {
                background-position: 5px 5px, 15px 15px, 25px 25px, 35px 35px;
            }
        }

        .title {
            text-align: center;
            font-size: 2.8em;
            font-weight: bold;
            color: #FFD700;
            text-shadow: 0 0 20px #FF8C00, 0 0 30px #FF8C00, 0 0 40px #FF8C00;
            margin-bottom: 0.5em;
        }

        .subtext {
            text-align: center;
            color: #eeeeeecc;
            font-size: 1.2em;
            margin-bottom: 2em;
        }

        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# App title and instructions
st.markdown('<div class="title">🪔 PaisaPaisa Layered Transaction Flowchart</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Upload a transaction Excel file and get a processed flowchart-style Excel as output.</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    with st.spinner("🔍 Processing your file..."):
        try:
            output_file = process_excel(uploaded_file)
            st.success("✅ File processed successfully!")
            st.download_button(
                label="📥 Download Output Excel",
                data=output_file,
                file_name=f"{uploaded_file.name.split('.')[0]}_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"❌ Error processing file: {e}")
