
📈 Statement Sifter
Extract expenses from PDF statements for a particular vendor and write them to Google Sheets.

🚀 Getting Started
🛠 Prerequisites
🐍 Python installed (version 3.x recommended).
📦 Required Python libraries. Run the following to get them:
Copy code
pip install -r requirements.txt
📑 Google Sheets API activated and service account credentials in place. (Don't worry, we guide you below!)
📝 Setting Up Google Sheets API
🌐 Go to Google Cloud Console.
🆕 Click on the project drop-down and select New Project. Give it a name.
🎛 Once the project is created, navigate to Enable APIs and Services.
🔍 Search for "Google Sheets API" and enable it.
🔐 After enabling, head over to the Credentials tab.
➕ Click on Create Credentials and choose Service account.
🖋 Fill out the fields to create the service account.
🗝 Post-creation, click on Edit for that account. Go to the Keys tab and click on Add Key. Choose JSON as the type. This downloads your credentials!
💌 Last but essential, share your Google Sheet with the email of the Service Account. You'll find this in your .json under client_email.
🏃‍♂️ Usage
📁 Rename the credentials to your_credentials.json and place them in the project directory.
🔗 Adjust source_folder in the script to point to your PDF statements' directory.
🖥 Run:
css
Copy code
python main.py
✨ Features
🧾 Efficient extraction of transactional data from PDF statements.
📊 Data neatly written to individual Google Sheets per statement.
💰 Provides a total sum of all your transactions.
🤝 Contributing
Wish to contribute? 🌟 Fork the repository, make your changes, and send in a pull request. All contributions are heartily welcome!

📜 License
MIT
