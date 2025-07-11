# 🌦️ Weather Alert System - Python WhatsApp Automation

⚠️ An automated climate alert system using **Python**, sending real-time **weather reports & alerts to WhatsApp Web**.  

Built for automation enthusiasts 🌟.

---

## ✅ Features
- 📊 4-Day Weather Forecast (Temperature, Condition)
- ⚠️ Climate Change Alerts:
  - Heat > 35°C
  - Cold < 5°C
  - Rain / Storm

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
```
git clone https://github.com/sathya3103/weather_alert_python
cd weather_alert_python
```
### 2️⃣ Setup Environment Variables
Create a .env file:
```
OWM_API_KEY=your_openweathermap_api_key
LATITUDE=your_latitude
LONGITUDE=your_longitude
```
Get your free API key: https://openweathermap.org/api

### 3️⃣ Install dependencies
```
pip install -r requirements.txt
```

### 4️⃣ Run the main script
```
python app.py
```
WhatsApp Web will open in your browser and send the message automatically after a few seconds.

### 🔍 Example Alert

<img width="618" height="530" alt="image" src="https://github.com/user-attachments/assets/1c02c0be-c8ab-46fa-83f2-bb4427c33232" />


---

### 📂 Folder Structure
```
weather_alert/
├── app.py                # Main runner script
├── scheduler.py          # Schedules alert + logging
├── weather.py            # Fetches forecasts + alerts
├── whatsapp.py           # WhatsApp sending logic
├── .env                  # API keys and location
├── requirements.txt      # Required libraries
└── PyWhatKit_DB.txt      # PyWhatKit internal DB

```

---
![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)


### 🙌 Contributions Welcome
Fork this repo, open an issue or PR!
