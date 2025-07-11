from scheduler import weather_alert
import schedule
import time

# Run every 1 hour
schedule.every(1).hours.do(weather_alert)

print("⏰ Weather Alert running every 1 hour...")

while True:
    schedule.run_pending()
    time.sleep(1)
