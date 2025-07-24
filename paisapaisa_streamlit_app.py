import streamlit as st
from paisapaisa_core import process_excel
import base64

# Set custom background using your sunset image
def set_background():
    img_base64 = (
        "data:image/jpeg;base64,"
        "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwg"
        "JC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIy"
        "MjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIy"
        # truncated for readability, full base64 is already embedded in your session
    )
    page_bg = f"""
    <style>
    .stApp {{
        background-image: url("{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

# Title with glow effect in one line
def title_with_glow():
    st.markdown("""
        <h1 style='text-align: center; color: #FFD700; 
            text-shadow: 0 0 10px #FFD700, 0 0 20px #FF8C00, 0 0 30px #FF8C00; 
            font-size: 3em; font-weight: bold;'>
            🍢 PaisaPaisa Layered Transaction Flowchart
        </h1>
    """, unsafe_allow_html=True)

def main():
    set_background()
    title_with_glow()

    st.markdown(
        "<p style='text-align: center; color: white; font-size: 1.2em;'>"
        "Upload a transaction Excel file and get a processed flowchart-style Excel as output."
        "</p>",
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
    if uploaded_file is not None:
        with st.spinner("Processing..."):
            output_file = process_excel(uploaded_file)
            st.success("Processing complete! Download your file below.")
            st.download_button(
                label="📥 Download Output Excel",
                data=output_file,
                file_name=uploaded_file.name.replace(".xlsx", "_output.xlsx"),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

if __name__ == "__main__":
    main()
