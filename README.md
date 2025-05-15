# VistoBot 🇺🇸🤖

An automated bot that checks for earlier available appointment dates for U.S. visa interviews on the official website ([https://ais.usvisa-info.com](https://ais.usvisa-info.com)) and sends an email alert if any date earlier than your currently scheduled one is found.

---

## 🚀 Features

* Automatically logs into the U.S. visa portal
* Navigates to the appointment rescheduling page
* Scans the calendar for available dates
* Compares those dates with the current scheduled date
* Sends email alerts when earlier dates are found
* Writes execution logs to `vistobot.log`
* Supports headless mode (runs without opening a browser window)
* Can be scheduled to run automatically using Windows Task Scheduler

---

## 🛠️ Requirements

* Python 3.11+ or 3.13
* Google Chrome installed
* ChromeDriver matching your Chrome version
* Gmail account with App Password authentication enabled

### Install dependencies:

```bash
pip install selenium python-dotenv
```

---

## 📁 Project structure

```
USembassy/
├── main.py              # Main bot script
├── .env                 # Environment variables (DO NOT upload to GitHub)
├── chromedriver.exe     # ChromeDriver binary
├── vistobot.log         # Log file with execution history
```

---

## 🔐 .env configuration

Create a `.env` file with the following content:

```
CSRA_USER=your_login_email
CSRA_PASS=your_portal_password
EMAIL_FROM=youremail@gmail.com
EMAIL_TO=youremail@gmail.com
EMAIL_PASS=your_app_password
```

> 💡 Use a [Gmail app password](https://myaccount.google.com/apppasswords) — this requires enabling 2FA.

---

## 🧠 How it works

1. The script logs into the visa scheduling portal
2. It navigates directly to the appointment rescheduling page
3. It reads the calendar using Selenium
4. Converts available dates to `datetime` objects
5. Compares them to your current appointment date
6. Sends an email if any earlier dates are found

---

## 🧪 Run manually

```bash
python main.py
```

> To watch the automation in action, **comment out** the `--headless=new` line in `main.py`.

---

## ⏰ Schedule it (Windows)

Use **Windows Task Scheduler**:

1. Open "Task Scheduler"
2. Click "Create Task"
3. Set up:

   * **Triggers**: 3 times daily (e.g., 08:00, 12:00, 22:00)
   * **Actions**:

     * Program: full path to `python.exe` (e.g., `C:\Python\Python311\python.exe`)
     * Argument: `"C:\...\main.py"`
     * Start in: directory of the script
   * Check "Run with highest privileges"

---

## 🧾 Sample log (`vistobot.log`)

```
[2025-05-15 08:00:00] 🚀 Starting VistoBot...
[2025-05-15 08:00:03] ☑️ Terms and conditions checkbox marked
[2025-05-15 08:00:06] 🔐 Successfully logged in
[2025-05-15 08:00:10] 📆 Rebooking page accessed
[2025-05-15 08:00:11] 🔍 No earlier dates found
[2025-05-15 08:00:12] 🏁 Execution finished
```

---

## 🔒 Safety

* The bot **never clicks to reschedule** — it only reads available dates.
* All operations are read-only; you decide whether to reschedule manually.
* Credentials are stored in a local `.env` file (never commit this).

---

## 📈 Possible future improvements

* Store a history of available dates in `.csv`
* Take screenshots when earlier dates are found
* Web dashboard using Flask or Streamlit
* Deploy to the cloud (AWS Lambda, EC2, etc.)

---

## 🧠 Author

Developed by Mikael Vestri with full-stack support from ChatGPT — powered by caffeine and a burning desire to never check that visa calendar manually again. ☕💼🇺🇸
