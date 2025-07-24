import streamlit as st
from paisapaisa_core import process_excel  # Your core logic
from io import BytesIO

# Set page config
st.set_page_config(
    page_title="PaisaPaisa Layered Flow",
    layout="centered",
)

# Custom background and styling
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("bg.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

h1 {
    font-size: 3.5em !important;
    color: black;
    text-shadow: 2px 2px 8px orange;
    text-align: center;
    margin-top: 20px;
    margin-bottom: 10px;
}

.upload-section {
    background-color: rgba(0, 0, 0, 0.5);
    padding: 2em;
    border-radius: 15px;
    margin-top: 30px;
}

.stButton > button {
    background-color: orange;
    color: black;
    border-radius: 10px;
    font-weight: bold;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Heading
st.markdown("<h1>🌅 PaisaPaisa Layered Transaction Flowchart</h1>", unsafe_allow_html=True)

# File upload
with st.container():
    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

    if uploaded_file is not None:
        with st.spinner("Processing..."):
            output_excel = process_excel(uploaded_file)

            # Download button
            st.success("Processing complete!")
            st.download_button(
                label="📥 Download Output Excel",
                data=output_excel,
                file_name=uploaded_file.name.replace('.xlsx', '_output.xlsx'),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
