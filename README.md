# 📊 Statement Sifter
> Extract expenses from PDF statements for a specific vendor and write them to Google Sheets.

## 🚀 Getting Started

### 🛠 Prerequisites
1. **Python**: Ensure you have Python installed (version 3.x recommended).
2. **Python Libraries**: You'll need to install certain libraries. You can do this using pip:
    ```bash
    pip3 install -r requirements.txt
    ```

### 📝 Setting up Google Sheets API
1. Go to the [Google Developers Console](https://console.developers.google.com/).
2. Create a new project.
3. Search for the Google Sheets API and enable it.
4. Create credentials for a Service Account.
6. Download the JSON file.
7. Move the downloaded JSON file to your project directory and rename it to `your_credentials.json`.

## 🏃 Running the Script
1. Place your PDF statements in the project directory.
2. Run the script:
    ```bash
    python3 main.py
    ```

3. Check your Google Sheets for the extracted expenses.

## 📈 Features
- 🧾 Efficient extraction of transactional data from PDF statements.
- 📊 Data neatly written to individual Google Sheets per statement.
- 💰 Provides a total sum of all your transactions.

## 💡 Contributing
Want to contribute? 🌟 Fork the repository, make your changes, and send in a pull request. All contributions are heartily welcome!

## 📜 License
[MIT](https://choosealicense.com/licenses/mit/)
