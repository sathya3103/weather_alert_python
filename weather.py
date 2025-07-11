import requests, os, datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OWM_API_KEY")
LAT = os.getenv("LATITUDE")
LON = os.getenv("LONGITUDE")

# ---- Helpers ----
def check_alerts(desc, temp, humidity, uvi, aqi):
    alerts = []
    if "rain" in desc.lower() or "storm" in desc.lower():
        alerts.append("⚠️ Rain/Storm Alert")
    if temp >= 35:
        alerts.append("🔥 Heat Alert")
    if temp <= 5:
        alerts.append("❄️ Cold Alert")
    if humidity >= 80:
        alerts.append("🌫️ High Humidity Alert")
    if uvi > 6:
        alerts.append("☀️ UV Exposure Alert")
    if aqi > 100:
        alerts.append("🌫️ Poor Air Quality Alert")
    return alerts

# ---- Fetch AQI ----
def get_air_quality():
    aqi_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"
    aqi_data = requests.get(aqi_url).json()
    try:
        return aqi_data["list"][0]["main"]["aqi"] * 50  # Convert to approx scale
    except:
        return 0

# ---- Fetch UV ----
def get_uvi():
    onecall_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={LAT}&lon={LON}&appid={API_KEY}"
    data = requests.get(onecall_url).json()
    return data.get("current", {}).get("uvi", 0)

# ---- Main Forecast ----
def get_weather_forecast():
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    if data.get("cod") != "200":
        return "❌ Failed to fetch weather data."

    aqi = get_air_quality()
    uvi = get_uvi()

    report = "🌦️ 4-Day Weather Forecast:\n\n"

    for item in data.get("list", [])[:32:8]:
        date = item["dt_txt"].split()[0]
        temp = item["main"]["temp"]
        humidity = item["main"]["humidity"]
        desc = item["weather"][0]["description"]

        alerts = check_alerts(desc, temp, humidity, uvi, aqi)

        report += f"📅 {date}\nTemp: {temp}°C | Humidity: {humidity}% | Condition: {desc}\n"
        if alerts:
            report += "🚨 Alerts: " + ", ".join(alerts) + "\n"
        report += "\n"

    location_link = f"https://www.google.com/maps?q={LAT},{LON}"
    report += f"📍 Location: {location_link}"

    return report, {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": temp,
        "humidity": humidity,
        "uvi": uvi,
        "aqi": aqi,
        "alerts": alerts,
        "weather": desc
    }