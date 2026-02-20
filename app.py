import schedule
import time
from scheduler import weather_alert

print("⏰ Weather Alert running every 1 minute (quick-check mode)...")
schedule.every(1).minutes.do(weather_alert)

while True:
    schedule.run_pending()
    time.sleep(1)