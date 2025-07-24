import streamlit as st
import pandas as pd
import base64
import io
from openpyxl import Workbook
from openpyxl.styles import PatternFill

# 🔥 Custom CSS with one-line title and strong glow
st.markdown("""
    <style>
        html, body, [class*="css"] {
            background-color: #0e0e0e !important;
        }

        .title-box {
            text-align: center;
            margin-top: 30px;
            margin-bottom: 0px;
        }

        .title-glow {
            font-size: 40px;
            font-weight: 900;
            color: #ffcc00;
            text-shadow:
                0 0 10px #ffcc00,
                0 0 20px #ff9900,
                0 0 30px #ff6600,
                0 0 40px #ff3300,
                0 0 55px #ff0000;
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

# One-line glowing title
st.markdown("""
    <div class="title-box">
        <div class="title-gl
