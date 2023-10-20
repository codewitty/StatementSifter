# 📊 Statement Sifter
> Extract expenses from PDF statements for a specific vendor and write them to Google Sheets.

## 🚀 Getting Started

### 🛠 Prerequisites
1. **Python**: Ensure you have Python installed (version 3.x recommended).
2. **Python Libraries**: You'll need to install certain libraries. You can do this using pip:
    ```bash
    pip install pdfplumber gspread oauth2client
    ```

### 📝 Setting up Google Sheets API
1. Go to the [Google Developers Console](https://console.developers.google.com/).
2. Create a new project.
3. Search for the Google Sheets API and enable it.
4. Create credentials for a Web server to access Application Data.
5. Choose Web server and Application data.
6. Download the JSON file.
7. Move the downloaded JSON file to your project directory and rename it to `your_credentials.json`.

## 🏃 Running the Script
1. Place your PDF statements in the project directory.
2. Run the script:
    ```bash
    python main.py
    ```

3. Check your Google Sheets for the extracted expenses.

## 📈 Features
- Extracts expense date and amount from PDF statements.
- Writes data to separate sheets in a Google Sheets document for each statement.

## 💡 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

## 📜 License
[MIT](https://choosealicense.com/licenses/mit/)
