import requests, os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OWM_API_KEY")
LAT = os.getenv("LATITUDE")
LON = os.getenv("LONGITUDE")

def check_for_alert(weather_description, temperature):
    alerts = []
    if "storm" in weather_description.lower() or "rain" in weather_description.lower():
        alerts.append("⚠️ Rain/Storm Alert")
    if temperature >= 35:
        alerts.append("🔥 Heat Alert")
    if temperature <= 5:
        alerts.append("❄️ Cold Alert")
    return alerts

def get_weather_forecast():
    if not all([API_KEY, LAT, LON]):
        return "❌ Missing API_KEY, LATITUDE, or LONGITUDE in .env file."

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        return f"❌ Error fetching weather data: {e}"

    if data.get("cod") != "200":
        return "❌ Failed to fetch weather data."

    forecast_list = data.get("list", [])
    report = "🌦️ 4-Day Weather Forecast:\n\n"

    for item in forecast_list[:8*4:8]:
        dt_txt = item['dt_txt'].split(" ")[0]
        temp = item['main']['temp']
        weather_desc = item['weather'][0]['description']
        alerts = check_for_alert(weather_desc, temp)

        report += f"📅 {dt_txt}\n"
        report += f"Temp: {temp}°C | Condition: {weather_desc}\n"
        if alerts:
            report += "🚨 Alerts: " + ", ".join(alerts) + "\n"
        report += "\n"

    location = f"https://www.google.com/maps?q={LAT},{LON}"
    report += f"📍 Location: {location}"

    return report
