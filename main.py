import pdfplumber
import re
import os
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

# Configuration for Google Sheets API
SCOPE = [
    "https://spreadsheets.google.com/feeds", 
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file", 
    "https://www.googleapis.com/auth/drive"
]

# Establish a connection with Google Sheets API
CREDS = ServiceAccountCredentials.from_json_keyfile_name('your_credentials.json', SCOPE)
CLIENT = gspread.authorize(CREDS)

def process_pdf(file_path):
    """Extract transaction data from a given PDF.
    
    Args:
        file_path (str): The path to the PDF file.
        
    Returns:
        tuple: List of transactions and the total amount spent.
    """
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
    """Convert file name to a human-readable statement name.
    
    Args:
        file_name (str): The original file name.
        
    Returns:
        str: Formatted statement name.
    """
    month_map = {
        "01": "January", "02": "February", "03": "March",
        "04": "April",   "05": "May",      "06": "June",
        "07": "July",    "08": "August",   "09": "September",
        "10": "October", "11": "November", "12": "December"
    }
    
    match = re.search(r'_([01][0-9])([12][0-9]{3})_', file_name)
    if match:
        month, year = match.groups()
        return f"{month_map[month]} {year}"
    return "Unknown Statement"

def get_or_create_worksheet(spreadsheet, title):
    """Fetch or create a new worksheet.
    
    Args:
        spreadsheet (obj): The target Google Sheets file.
        title (str): Desired worksheet name.
        
    Returns:
        obj: A worksheet instance.
    """
    try:
        return spreadsheet.worksheet(title)
    except gspread.WorksheetNotFound:
        return spreadsheet.add_worksheet(title=title, rows="100", cols="5")

def write_to_google_sheet(data, total, statement_name, sheet_name):
    """Write the processed data to a Google Sheet.
    
    Args:
        data (list): List of transaction data.
        total (float): Total amount of the transactions.
        statement_name (str): The name of the statement.
    """
    spreadsheet = CLIENT.open(sheet_name)
    sheet_name = format_statement_name(statement_name)
    sheet = get_or_create_worksheet(spreadsheet, sheet_name)
    
    # Clear the current sheet data
    sheet.clear()

    # Write header row
    sheet.append_row(["Date", "Amount"])

    for date, amount in data:
        sheet.append_row([date, amount])
        time.sleep(1)
    sheet.append_row(['Total', total])

# Execution starts here
if __name__ == "__main__":
    SOURCE_FOLDER = './'
    
    for file_name in os.listdir(SOURCE_FOLDER):
        if file_name.endswith('.pdf'):
            data, total = process_pdf(os.path.join(SOURCE_FOLDER, file_name))
            write_to_google_sheet(data, total, "YOUR_SHEET_NAME")

