from scheduler import weather_alert
import sys

def run_test():
    print("🚀 Manual Trigger: Fetching weather and sending WhatsApp alert...")
    try:
        weather_alert()
        print("\n✅ Process finished successfully.")
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_test()
