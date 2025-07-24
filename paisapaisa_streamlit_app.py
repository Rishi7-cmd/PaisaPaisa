import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="PaisaPaisa Flowchart", layout="centered")

# Diwali-themed background and header
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top, #2c2c2c 0%, #0a0a0a 100%) !important;
        color: #ffffff;
    }

    h1 {
        color: #ffcc00;
        font-size: 3em;
        text-shadow: 0 0 10px #ffd700, 0 0 20px #ffaa00;
        font-weight: 900;
        text-align: center;
    }

    body::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 120px;
        background: url('https://i.imgur.com/OT3rI6z.png') repeat-x;
        z-index: 9999;
        pointer-events: none;
        animation: flicker 2s infinite;
    }

    @keyframes flicker {
        0%, 100% { opacity: 0.8; }
        50% { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🪔 PaisaPaisa Layered Transaction Flowchart</h1>", unsafe_allow_html=True)
st.write("Upload a transaction Excel file and get a processed flowchart-style Excel as output.")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

def process_excel(input_file, base_filename):
    df = pd.read_excel(input_file)
    
    # --- Apply filters ---
    df = df[df["Amount"] > 50000]
    df = df[df["Layer"] <= 2]
    df = df[df["Withdrawal"] > 0]

    # --- Highlight withdrawals over 1 lakh ---
    def highlight(val):
        return 'background-color: #ff6666' if val > 100000 else ''
    
    styled_df = df.style.applymap(highlight, subset=["Withdrawal"])

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        styled_df.to_excel(writer, index=False, sheet_name="Filtered Data")
    
    output.seek(0)
    return output

if uploaded_file:
    base_name = uploaded_file.name.rsplit(".", 1)[0]
    output_buffer = process_excel(uploaded_file, base_name)

    st.success("✅ File processed successfully!")
    st.download_button(
        label="📥 Download Processed Excel",
        data=output_buffer,
        file_name=f"{base_name}_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
