# 🌦️ Weather Alert System - Python WhatsApp Automation

⚠️ An automated climate alert system using **Python**, sending real-time **weather reports & alerts to WhatsApp Web**.  

Built for Hackathons and automation enthusiasts 🌟.

---

## ✅ Features
- 📊 4-Day Weather Forecast (Temperature, Condition)
- ⚠️ Climate Change Alerts:
  - Heat > 35°C
  - Cold < 5°C
  - Rain / Storm
- 🌫️ Advanced Alerts:
  - Humidity > 80%
  - UV Index > 6
  - Air Quality Index (AQI) > 100
- 📍 Live location link (Google Maps)
- 💬 WhatsApp Web integration using **PyWhatKit**
- 🔁 Fully automatic: can run hourly from VSCode terminal

---

## 🔧 Tech Stack
- **Python 3.10+**
- OpenWeatherMap API
- PyWhatKit (WhatsApp Automation)
- dotenv (Environment Variables)

---

## 🚀 How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/sathya3103/weather_alert_python
cd weather_alert_python

###2️⃣ Setup Environment Variables
```bash
Create a .env file:
OWM_API_KEY=your_openweathermap_api_key
LATITUDE=your_latitude
LONGITUDE=your_longitude

Get your free API key: https://openweathermap.org/api

###3️⃣ Install dependencies
```bash
pip install -r requirements.txt

4️⃣ Run the main script
```bash
python app.py
WhatsApp Web will open in your browser and send the message automatically after a few seconds.

🔍 Example Alert

🌦️ 4-Day Weather Forecast:

📅 2025-07-11
Temp: 36°C | Humidity: 82% | Condition: light rain
🚨 Alerts: 🌫️ High Humidity Alert, 🔥 Heat Alert, ⚠️ Rain Alert

📅 2025-07-12
Temp: 34°C | Humidity: 60% | Condition: clear sky

📍 Location: https://www.google.com/maps?q=12.9716,77.5946

📂 Folder Structure
weather_alert/
├── app.py                # Main runner script
├── scheduler.py          # Schedules alert + logging
├── weather.py            # Fetches forecasts + alerts
├── whatsapp.py           # WhatsApp sending logic
├── .env                  # API keys and location
├── requirements.txt      # Required libraries
└── PyWhatKit_DB.txt      # PyWhatKit internal DB

🙌 Contributions Welcome
Fork this repo, open an issue or PR!
