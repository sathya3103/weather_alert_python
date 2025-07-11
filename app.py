import schedule
import time
from scheduler import weather_alert

print("⏰ Weather Alert running every 1 hour...")
schedule.every(1).minutes.do(weather_alert)

while True:
    schedule.run_pending()
    time.sleep(1)