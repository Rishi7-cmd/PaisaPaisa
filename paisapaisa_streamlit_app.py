import streamlit as st
from paisapaisa_core import process_excel
from io import BytesIO

st.set_page_config(
    page_title="PaisaPaisa Layered Flow",
    layout="centered"
)

# Custom Diwali background and styling
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0d0d0d;
    background-image: radial-gradient(#ffaa00 1px, transparent 1px),
                      radial-gradient(#ffaa00 1px, transparent 1px);
    background-size: 40px 40px;
    background-position: 0 0, 20px 20px;
}

h1 {
    color: #ffcc00;
    text-align: center;
    font-size: 3em;
    font-weight: bold;
    text-shadow: 0 0 10px #ffaa00, 0 0 20px #ffaa00, 0 0 30px #ffaa00;
    margin-top: 20px;
    margin-bottom: 30px;
}

.stFileUploader, .stButton > button {
    background-color: #1a1a1a;
    border: 1px solid #ffaa00;
    color: #ffaa00;
    border-radius: 10px;
    padding: 10px;
    font-weight: bold;
}

.stDownloadButton > button {
    background-color: #ffaa00;
    color: black;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 20px;
}

.stMarkdown {
    color: #ffcc00;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Title
st.markdown("<h1>🪔 PaisaPaisa Layered Transaction Flow</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    with st.spinner("Processing file..."):
        output = process_excel(uploaded_file)

        st.success("✅ Done! Click below to download:")
        st.download_button(
            label="📥 Download Processed Excel",
            data=output,
            file_name=uploaded_file.name.replace('.xlsx', '_output.xlsx'),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
