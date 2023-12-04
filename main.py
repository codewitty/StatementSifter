
import pdfplumber
import re
import os
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Set up the Google Sheets credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

def update_summary_sheet(spreadsheet, monthly_totals):
    summary_sheet_title = "Monthly Totals"
    summary_sheet = get_or_create_worksheet(spreadsheet, summary_sheet_title)

    # Get existing data
    existing_data = summary_sheet.get_all_values()

    # Preserve the header row and all but the last row (grand total)
    header_row = existing_data[0]
    preserved_data = existing_data[1:-1]

    grand_total = float(existing_data[-1][-1]) if existing_data else 0.0  # Get the previous grand total

    # Clear existing data (except header row)
    summary_sheet.clear()
    summary_sheet.append_row(header_row)

    # Add new monthly totals and update the grand total
    for month, total in monthly_totals.items():
        preserved_data.append([month, total])
        grand_total += total

    # Append the new grand total
    preserved_data.append(["Grand Total", grand_total])

    # Write the updated data to the sheet
    summary_sheet.insert_rows(preserved_data, 2)

def process_pdf(file_path):
    transactions = []
    total_spent = 0.0

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages[2:]:
            text = page.extract_text()
            charges = re.findall(r'(\w+ \d+ \w+ \d+ FACEBK [^\n]+ \$\d+\.\d+)', text)

            for charge in charges:
                date_match = re.search(r'(\w+ \d+)', charge)
                amount_match = re.search(r'\$(\d+\.\d+)', charge)

                if date_match and amount_match:
                    date = date_match.group(0)
                    amount = float(amount_match.group(1))
                    transactions.append((date, amount))
                    total_spent += amount

    return transactions, total_spent

def format_statement_name(file_name):
    month_map = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December"
    }

    # Extract month and year from the filename using regex
    match = re.search(r'_([01][0-9])([12][0-9]{3})_', file_name)
    if match:
        month, year = match.groups()
        return f"{month_map[month]} {year}"
    return "Unknown Statement"

def get_or_create_worksheet(spreadsheet, title):
    try:
        return spreadsheet.worksheet(title)
    except gspread.WorksheetNotFound:
        return spreadsheet.add_worksheet(title=title, rows="100", cols="5")

def write_to_google_sheet(data, total, statement_name):
    spreadsheet = client.open("Test")
    sheet_name = format_statement_name(statement_name)
    sheet = get_or_create_worksheet(spreadsheet, sheet_name)

    # Clear the current sheet data
    sheet.clear()

    # Write header row
    sheet.append_row(["Date", "Amount"])

    # Rate limiting: sleep for 1 second after every write to avoid quota exceeded errors
    for date, amount in data:
        sheet.append_row([date, amount])
        time.sleep(1)
    sheet.append_row(['Total', total])

# Main
if __name__ == "__main__":
    source_folder = './'
    monthly_totals = {}

    for file_name in os.listdir(source_folder):
        if file_name.endswith('.pdf'):
            data, total = process_pdf(os.path.join(source_folder, file_name))
            write_to_google_sheet(data, total, file_name)
            sheet_name = format_statement_name(file_name)
            monthly_totals[sheet_name] = total

    update_summary_sheet(client.open("Test"), monthly_totals)

