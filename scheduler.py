from weather import get_weather_forecast
from whatsapp import send_whatsapp
import json

LOG_FILE = "logs.json"

def save_log(log_data):
    try:
        with open(LOG_FILE, "r") as file:
            logs = json.load(file)
    except:
        logs = []

    logs.append(log_data)

    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=2)

def weather_alert():
    report, log_data = get_weather_forecast()
    print(report)
    send_whatsapp(report)
    save_log(log_data)
