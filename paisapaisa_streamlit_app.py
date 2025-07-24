import streamlit as st
import pandas as pd
import io
from paisapaisa_core import process_excel

# Set custom background using CSS
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("bg.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .main-title {
        font-size: 50px;
        font-weight: bold;
        color: #000000;
        text-shadow: 0 0 10px #FFD700, 0 0 20px #FFA500;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">💸 Paisa Paisa Forensics</div>', unsafe_allow_html=True)
st.write("")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    try:
        output_df = process_excel(uploaded_file)
        st.success("✅ File processed successfully!")
        st.dataframe(output_df)

        # Prepare Excel download
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            output_df.to_excel(writer, index=False)
        buffer.seek(0)

        st.download_button(
            label="📥 Download Processed Excel",
            data=buffer,
            file_name="processed_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
