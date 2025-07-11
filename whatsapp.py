import pywhatkit
import os
from dotenv import load_dotenv

load_dotenv()

PHONE = os.getenv("PHONE_NUMBER")

def send_whatsapp(message):
    pywhatkit.sendwhatmsg_instantly(PHONE, message)
    print("✅ WhatsApp message sent instantly.")
