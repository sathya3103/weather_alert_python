# 🌦️ WhatsApp Weather Alert Automation

A Python-based automation system that fetches a 4-day weather forecast from OpenWeatherMap, detects simple alert conditions (heat, cold, rain), formats a human-readable report, and delivers it to a configured WhatsApp contact using browser automation.

Designed for personal use / low-volume alerting, with multiple fallback strategies to maximize delivery reliability.

---

## 📌 Project Overview

This project:

- Periodically fetches weather data using the OpenWeatherMap API
- Analyzes forecast data for alert conditions
- Formats a concise, readable weather report
- Sends alerts automatically via WhatsApp Web
- Uses multiple delivery strategies for resilience
- Supports quick-test mode (1-minute scheduling) and hourly production mode

---

## 🏗️ Architecture

```

app.py
↓
scheduler.py
↓
weather.py  →  OpenWeatherMap API
↓
whatsapp.py →  Chrome / Selenium / PyWhatKit

```

### Core Flow

1. Scheduler triggers weather check.
2. Weather module fetches 4-day forecast.
3. Alert logic determines:
   - Heat threshold
   - Cold threshold
   - Rain probability
4. Message formatted.
5. WhatsApp delivery attempted via layered fallback system.

---

## 📂 Project Structure

| File | Purpose |
|------|----------|
| `app.py` | Main entry point and scheduler runner |
| `scheduler.py` | Orchestrates fetching forecast and sending alerts |
| `weather.py` | OpenWeatherMap integration, alert logic, formatting |
| `whatsapp.py` | WhatsApp sending strategies and helpers |
| `requirements.txt` | Dependency list |
| `.env` | Environment variables (not committed) |

---

## ⚙️ Features

### 🌡 Weather Processing
- 4-day forecast retrieval
- Alert detection:
  - High temperature
  - Low temperature
  - Rain prediction
- Clean human-readable formatting

### 📲 WhatsApp Delivery (Multi-Strategy)

Delivery attempts follow this priority order:

1. **Remote Debug Attach (Fastest)**
   - Attaches to already-running Chrome session
   - ~2–5 second delivery
2. **Selenium Fast Mode**
   - Reuses Chrome profile
3. **PyWhatKit Instant Mode**
   - `sendwhatmsg_instantly()`
4. **PyWhatKit Scheduled Fallback**
   - Scheduled ≥120 seconds ahead to avoid sleep errors
5. **Diagnostic Mode**
   - Captures screenshot for troubleshooting

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
OWM_API_KEY=your_openweathermap_api_key
LATITUDE=12.9716
LONGITUDE=77.5946
PHONE_NUMBER=+91XXXXXXXXXX

# Optional (for Selenium fast send)
CHROME_PROFILE_PATH=C:\Users\<your-user>\AppData\Local\Google\Chrome\User Data
```

### Required

| Variable       | Description                               |
| -------------- | ----------------------------------------- |
| `OWM_API_KEY`  | OpenWeatherMap API key                    |
| `LATITUDE`     | Decimal latitude                          |
| `LONGITUDE`    | Decimal longitude                         |
| `PHONE_NUMBER` | Recipient WhatsApp number in E.164 format |

### Optional

| Variable              | Description                |
| --------------------- | -------------------------- |
| `CHROME_PROFILE_PATH` | Chrome user-data directory |

---

## 🧰 Dependencies

### Core

* requests
* schedule
* pywhatkit
* python-dotenv

### Optional (Recommended)

* selenium
* webdriver-manager

Install with:

```bash
pip install -r requirements.txt
```

---

## 🚀 Installation & Setup

### 1️⃣ Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2️⃣ Configure Environment Variables

Create `.env` with required values.

### 3️⃣ Run Scheduler

```bash
python app.py
```

---

## 🧪 Quick Test Commands

### Forecast Only

```bash
.\venv\Scripts\python.exe -c "from weather import get_weather_forecast; print(get_weather_forecast())"
```

### Test WhatsApp Send

```bash
.\venv\Scripts\python.exe -c "from whatsapp import send_whatsapp; send_whatsapp('Test message')"
```

---

## 🖥️ Chrome Fast Mode (Recommended)

Start Chrome manually with remote debugging:

```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\<your-user>\ChromeAutomationProfile"
```

Benefits:

* Instant attach
* No QR re-scan
* Fastest delivery method

---

## ⏱ Scheduler Modes

### Quick Check (Testing Mode)

Runs every 1 minute:

```python
schedule.every(1).minutes.do(weather_alert)
```

### Production Mode (Recommended)

Runs hourly:

```python
schedule.every().hour.do(weather_alert)
```

---

## 🧠 Alert Logic

Alert conditions evaluated against forecast data:

* Temperature > heat threshold
* Temperature < cold threshold
* Rain probability > threshold
* Aggregated across forecast window

Example Output:

```
Weather Alert 🌦️

Day 1: 34°C – Sunny
Day 2: 29°C – Rain expected
Day 3: 31°C – Cloudy
Day 4: 33°C – Clear

⚠️ Rain expected in next 48 hours.
```

---

## 🛠 Troubleshooting

### PyWhatKit Error

```
sleep length must be non-negative
```

Fix: Ensure scheduled time ≥120 seconds ahead.

---

### Selenium DevTools Error

Occurs if Chrome is already using the same profile.

Fix:

* Close all Chrome windows
  OR
* Use remote-debug attach method.

---

### WhatsApp QR Reappears

Ensure:

* Chrome profile has active WhatsApp Web session.
* Use dedicated automation profile.

---

### Debug Mode

```python
send_whatsapp_debug()
```

Captures:

* Screenshot
* Page diagnostics
* Session state information

---

## 🔒 Security Notes

* Never commit `.env`
* Keep API keys private
* Use separate Chrome profile for automation
* Browser automation is fragile and not production-grade

---

## ⚠️ Limitations

* Depends on WhatsApp Web UI (may break if UI changes)
* Not suitable for high-volume messaging
* Requires Chrome + local runtime
* Delivery timing depends on machine/network speed

---

## 🏢 Production Recommendation

For scalable deployment:

➡️ Use WhatsApp Business Cloud API instead of browser automation.

Advantages:

* Official support
* Reliable delivery
* No UI dependency
* Production-grade scalability

---

## 🔮 Future Improvements

* Unit tests for weather parsing
* Structured logging (file + levels)
* Retry with exponential backoff
* Persistent job tracking (database)
* Docker containerization
* Cloud/VPS deployment

---

## 📜 License

MIT License

---

## 👨‍💻 Author

Personal automation project for intelligent weather alerting via WhatsApp.
