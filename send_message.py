import csv
import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import config
# Firebase Credentials & Local Storage
FIREBASE_CRED = config.FIREBASE_CRED
SYSTEM_INFO_FILE = config.SYSTEM_INFO_FILE
LOCAL_MESSAGES_FILE = config.LOCAL_MESSAGES_FILE

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CRED)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Function to read UID from CSV
def get_uid_from_csv():
    try:
        with open(SYSTEM_INFO_FILE, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                return row.get("UID", None)  # Only return the first UID found
    except Exception as e:
        print(f"❌ Error reading system info: {e}")
        return None

# Function to log messages locally
def log_message_locally(uid, tag, message, timestamp):
    try:
        with open(LOCAL_MESSAGES_FILE, mode="a", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            # If file is empty, write headers
            if csvfile.tell() == 0:
                writer.writerow(["UID", "Role", "Tag", "Message", "Timestamp"])
            writer.writerow([uid, "user", tag, message, timestamp])
    except Exception as e:
        print(f"❌ Error saving message locally: {e}")

# Function to send a message (single-line callable)
def send_message(tag, message, link=""):
    uid = get_uid_from_csv()  # Get UID from CSV
    if not uid:
        print("❌ Error: UID not found! Cannot send message.")
        return

    # Get current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Store message locally
    log_message_locally(uid, tag, message, timestamp)

    # Save message to Firestore under "messages" collection
    db.collection("messages").add({
        "uid": uid,
        "role": "user",  # Always "user"
        "tag": tag,
        "message": message,
        "link": link,
        "timestamp": timestamp
    })

    print(f"✅ Message from {uid} saved locally and sent successfully!")

