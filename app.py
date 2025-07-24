
import streamlit as st
from paisapaisa_core import process_excel
import base64

# Set page config
st.set_page_config(
    page_title="PaisaPaisa Flowchart Generator",
    layout="centered",
)

# Load and set background image
def set_bg_image(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set background
set_bg_image("bg.jpg")

# Title with glow
st.markdown("""
<h1 style='text-align: center; color: #FFD700; text-shadow: 0 0 10px #FFA500, 0 0 20px #FF8C00, 0 0 30px #FF4500;'>
🌭 PaisaPaisa Layered Transaction Flowchart
</h1>
""", unsafe_allow_html=True)

# Upload section
st.markdown("#### Upload a transaction Excel file and get a processed flowchart-style Excel as output.")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    output_path = process_excel(uploaded_file)
    with open(output_path, "rb") as f:
        st.download_button(
            label="📥 Download Processed Excel",
            data=f,
            file_name=Path(output_path).name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
