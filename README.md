# 🌦️ WhatsApp Weather Alert Automation

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Automation: Selenium](https://img.shields.io/badge/Automation-Selenium-green.svg)](https://www.selenium.dev/)
[![API: OpenWeather](https://img.shields.io/badge/API-OpenWeather-orange.svg)](https://openweathermap.org/)

An weather forecasting and notification system that delivers personalized 4-day weather alerts directly to your WhatsApp. Built with reliability in mind, it features a multi-layered delivery system to ensure you never miss an important update.

---

## 🚀 Key Features

*   **Forecasts**: Fetches 4-day granular data from OpenWeatherMap.
*   **Alerting**: Detects extreme temperatures (heat/cold) and rain probability.
*   **High-Fidelity Delivery**: Multi-strategy WhatsApp sending:
    *   **Remote Attach**: Lightning-fast (2-5s) delivery using an existing Chrome session.
    *   **Selenium Automation**: Fully automated browser control with profile persistence.
    *   **PyWhatKit Fallback**: Reliable backup delivery strategies.
*   **Professional Formatting**: Concise, emoji-rich reports with Google Maps location links.

---

## 📂 Project Structure

```text
weather_alert/
├── .env                # Secret environment variables
├── app.py              # Main entry point (Background Scheduler)
├── scheduler.py        # Logic coordinator
├── weather.py          # API integration & message formatting
├── whatsapp.py         # Advanced delivery engine
├── test_alert.py       # Instant test utility
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
```

---

## 🛠️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/sathya3103/weather_alert_python.git
cd weather_alert_python
```

### 2. Create Virtual Environment
```powershell
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install Dependencies
pip install -r requirements.txt
```

### 3. Configuration
Duplicate the configuration template or create a `.env` file in the root directory:

```env
OWM_API_KEY=your_api_key_here
PHONE_NUMBER=+91XXXXXXXXXX
LATITUDE=13.0827
LONGITUDE=80.2707

# Windows Path Example:
CHROME_PROFILE_PATH=C:\Users\<YourUser>\AppData\Local\Google\Chrome\User Data\Default
```

---

## 🚀 Usage

### Running the Background Scheduler
To start the automatic hourly alerts:
```powershell
python app.py
```

### Instant Test Run
To verify your setup and send an alert immediately:
```powershell
python test_alert.py
```

---

## 💡 Pro Tip: Instant WhatsApp Mode

For the fastest and most reliable delivery, run Chrome in **Remote Debugging Mode**. This allows the script to "piggyback" on your active browser without opening new windows.

1.  **Close Chrome** completely.
2.  Run this in **PowerShell**:
    ```powershell
    & "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\<YourUser>\AppData\Local\Google\Chrome\User Data"
    ```
3.  The script will now send alerts in **under 3 seconds**!

---

## ⚠️ Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **Profile Locked** | Close all Chrome windows or use the "Remote Debugging" command above. |
| **Selenium Error** | Run `taskkill /F /IM chromedriver.exe /T` and try again. |
| **QR Scan Needed** | Switch to PyWhatKit fallback or ensure you've scanned once in the automation profile. |

---

## 🔒 Security & Privacy

*   **API Security**: Never commit your `.env` file (it is already in `.gitignore`).
*   **Privacy**: This project uses Selenium to interact with your *local* browser sessions; no credentials leave your machine.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👨‍💻 Author

Developed for intelligent, automated weather notifications.
