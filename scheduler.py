from weather import get_weather_forecast
from whatsapp import send_whatsapp

def weather_alert():
    report = get_weather_forecast()
    print(report)
    send_whatsapp(report)
