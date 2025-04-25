#importations :
import os
import sys
from dotenv import load_dotenv
from whatsapp_manager import WhatsappManager
import time

    
print("Loading environment variables...")
load_dotenv()

# Get environment variables properly
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

if not all([ACCESS_TOKEN, RECIPIENT_WAID, PHONE_NUMBER_ID, VERSION]):
    print("missing variables: ", [var for var in ["ACCESS_TOKEN", "RECIPIENT_WAID", "PHONE_NUMBER_ID", "VERSION"] if not os.getenv(var)])


wa_manager = WhatsappManager(
    wa_id=RECIPIENT_WAID,  # Using recipient ID as the user ID, not PHONE_NUMBER_ID
    access_token=ACCESS_TOKEN,
    phone_number_id=PHONE_NUMBER_ID,
    api_version=VERSION)

print("Sending test message...")
response = wa_manager.send_message("Hello, this is a test message!")
print("Message sent successfully:", response.status_code)

# Record an incoming message
wa_manager.record_incoming("Hello, incoming message!")
print("Incoming message recorded successfully.")
print("Message history:", wa_manager.messages)
