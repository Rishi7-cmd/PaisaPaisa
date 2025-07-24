
import streamlit as st
import pandas as pd
import xlsxwriter
import io
import os

def process_excel(input_file, output_name):
    excel_data = pd.ExcelFile(input_file)
    df_main = excel_data.parse('Money Transfer to')

    df_main['Transaction Amount'] = df_main['Transaction Amount'].astype(str).str.replace(',', '')
    df_main['Transaction Amount'] = df_main['Transaction Amount'].astype(float)
    df_main_filtered = df_main[df_main['Transaction Amount'] > 50000].copy()
    df_main_filtered['Account No'] = df_main_filtered['Account No'].astype(str)

    withdraw_sheets = ['Withdrawal through ATM', 'Cash Withdrawal through Cheque', 'Withdrawal through POS', 'AEPS']
    withdrawal_frames = []
    for sheet in withdraw_sheets:
        if sheet not in excel_data.sheet_names:
            continue
        df = excel_data.parse(sheet)
        if 'Account No' in df.columns:
            account_col = 'Account No'
        else:
            account_col = 'Account No./ (Wallet /PG/PA) Id'
        if 'Withdrawal Amount' not in df.columns:
            continue
        df = df[[account_col, 'Withdrawal Amount']].copy()
        df.columns = ['Account No', 'Withdrawal Amount']
        df.dropna(inplace=True)
        df['Account No'] = df['Account No'].astype(str).str.extract(r'(\d+)')
        df['Withdrawal Amount'] = df['Withdrawal Amount'].astype(str).str.replace(',', '').astype(float)
        withdrawal_frames.append(df)

    withdrawals_combined = pd.concat(withdrawal_frames, ignore_index=True)
    withdraw_map = withdrawals_combined.groupby('Account No')['Withdrawal Amount'].max().to_dict()
    df_main_filtered['Withdrawal Done'] = df_main_filtered['Account No'].map(withdraw_map)

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Flowchart")

    victim_format = workbook.add_format({'bold': True, 'bg_color': '#87CEEB', 'align': 'center', 'valign': 'vcenter', 'border': 1})
    layer1_format = workbook.add_format({'bg_color': '#ADD8E6', 'align': 'center', 'valign': 'vcenter', 'border': 1, 'text_wrap': True})
    layer2_format = workbook.add_format({'bg_color': '#90EE90', 'align': 'center', 'valign': 'vcenter', 'border': 1, 'text_wrap': True})
    arrow_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'font_color': 'black'})
    withdraw_format = workbook.add_format({'bg_color': '#FFD700', 'align': 'center', 'valign': 'vcenter', 'border': 1, 'text_wrap': True})
    withdraw_high_format = workbook.add_format({'bg_color': '#FFD700', 'align': 'center', 'valign': 'vcenter', 'border': 1, 'bold': True, 'font_color': 'red', 'text_wrap': True})

    row = 0

    for victim, group in df_main_filtered.groupby("Acknowledgement No."):
        layer1_accounts = group[group["Layer"] == 1]
        layer2_accounts = group[group["Layer"] == 2]

        spacing = 2
        start_col = 0
        end_col = (len(layer1_accounts) - 1) * spacing
        worksheet.merge_range(row, start_col, row, end_col, f"Victim: {victim}", victim_format)

        row_l1 = row + 2
        row_arrow1 = row + 3
        row_l2 = row + 4
        row_arrow2 = row + 5
        row_withdraw = row + 6
        row_withdraw_l1 = row + 7

        for i, (_, l1_row) in enumerate(layer1_accounts.iterrows()):
            col = i * spacing
            l1_acc = l1_row["Account No"]

            l1_text = (
                f"Bank: {l1_row['Bank/FIs']}\n"
                f"A/c No: {l1_acc}\n"
                f"IFSC: {l1_row['Ifsc Code']}\n"
                f"Amount Sent: ₹{int(l1_row['Transaction Amount'])}"
            )
            worksheet.write(row_l1, col, l1_text, layer1_format)
            worksheet.write(row_arrow1, col, "↓", arrow_format)

            if not pd.isna(l1_row["Withdrawal Done"]):
                amt = l1_row["Withdrawal Done"]
                withdraw_text = (
                    f"💸 Withdrawal Made\n"
                    f"From: Layer 1\n"
                    f"A/c No: {l1_acc}\n"
                    f"Amount: ₹{int(amt)}"
                )
                fmt = withdraw_high_format if amt > 100000 else withdraw_format
                worksheet.write(row_withdraw_l1, col, withdraw_text, fmt)

            l2_matches = layer2_accounts[layer2_accounts["Account No./ (Wallet /PG/PA) Id"] == l1_acc]

            for _, l2_row in l2_matches.iterrows():
                l2_acc = l2_row["Account No"]
                l2_text = (
                    f"Bank: {l2_row['Bank/FIs']}\n"
                    f"A/c No: {l2_acc}\n"
                    f"IFSC: {l2_row['Ifsc Code']}\n"
                    f"Amount Received: ₹{int(l2_row['Transaction Amount'])}"
                )
                worksheet.write(row_l2, col, l2_text, layer2_format)
                worksheet.write(row_arrow2, col, "↓", arrow_format)

                if not pd.isna(l2_row["Withdrawal Done"]):
                    amt = l2_row["Withdrawal Done"]
                    withdraw_text = (
                        f"💸 Withdrawal Made\n"
                        f"From: Layer 2\n"
                        f"A/c No: {l2_acc}\n"
                        f"Amount: ₹{int(amt)}"
                    )
                    fmt = withdraw_high_format if amt > 100000 else withdraw_format
                    worksheet.write(row_withdraw, col, withdraw_text, fmt)

        row = row_withdraw_l1 + 4

    workbook.close()
    output.seek(0)
    return output

st.set_page_config(page_title="PaisaPaisa Flowchart Generator", layout="centered")

st.title("💸 PaisaPaisa Layered Transaction Flowchart")
st.markdown("Upload a transaction Excel file and get a processed flowchart-style Excel as output.")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    base_filename = os.path.splitext(uploaded_file.name)[0]
    output_buffer = process_excel(uploaded_file, base_filename + "_output.xlsx")
    st.success("✅ Processed successfully!")

    st.download_button(
        label="📥 Download Output Excel",
        data=output_buffer,
        file_name=base_filename + "_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
