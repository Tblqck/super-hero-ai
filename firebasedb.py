import csv
import firebase_admin
from firebase_admin import credentials, firestore
import config
# Firebase Credentials
FIREBASE_CRED = config.FIREBASE_CRED
SYSTEM_INFO_FILE = config.SYSTEM_INFO_FILE

# Initialize Firebase
cred = credentials.Certificate(FIREBASE_CRED)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Read system info from CSV
def read_system_info():
    system_info = {}
    try:
        with open(SYSTEM_INFO_FILE, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                system_info["UID"] = row.get("UID", "Unknown UID")
                system_info["OS"] = row.get("OS", "Unknown OS")
                system_info["OS Version"] = row.get("OS Version", "Unknown Version")
                system_info["Processor"] = row.get("Processor", "Unknown Processor")
                system_info["RAM"] = row.get("RAM", "Unknown RAM")
                system_info["Screen Resolution"] = row.get("Screen Resolution", "Unknown Resolution")
                break  # Only read the first row
    except Exception as e:
        print(f"Error reading system info: {e}")
        return None
    return system_info

# Function to register user in Firestore
def register_user():
    system_info = read_system_info()
    if not system_info:
        print("Error: Could not retrieve system info!")
        return

    # Check if UID already exists in Firestore
    user_ref = db.collection("users").document(system_info["UID"])
    if user_ref.get().exists:
        print(f"✅ User {system_info['UID']} already exists. Skipping registration.")
        return

    # Add user info to Firestore
    user_ref.set({
        "uid": system_info["UID"],
        "os": system_info["OS"],
        "os_version": system_info["OS Version"],
        "processor": system_info["Processor"],
        "ram": system_info["RAM"],
        "screen_resolution": system_info["Screen Resolution"],
        "role": "user"  # You can manually change to "admin" in Firestore if needed
    })

    print(f"✅ User {system_info['UID']} registered successfully!")

# Run registration once on app launch
register_user()
