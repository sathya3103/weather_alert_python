import pywhatkit
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

PHONE_NUMBER = os.getenv("PHONE_NUMBER")

def send_whatsapp(message):
    now = datetime.datetime.now()
    # Send after 2 minutes
    pywhatkit.sendwhatmsg(PHONE_NUMBER, message, now.hour, now.minute + 1)
    print("✅ WhatsApp message scheduled.")
