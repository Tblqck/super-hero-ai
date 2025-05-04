import hashlib
import platform
import uuid
import psutil
import screeninfo
import csv
import os

def get_system_uid():
    """Generates a unique system UID based on MAC address, CPU details, and Disk Serial Number."""
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 8)][::-1])
    cpu = platform.processor()
    disk_serial = psutil.disk_partitions()[0].device if psutil.disk_partitions() else "unknown"
    
    unique_string = f"{mac}-{cpu}-{disk_serial}"
    uid = hashlib.sha256(unique_string.encode()).hexdigest()
    
    return uid

def get_system_specs():
    """Retrieves system specifications including OS, CPU, and RAM."""
    return {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Processor": platform.processor(),
        "RAM": f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB"
    }

def get_screen_resolution():
    """Gets the primary screen resolution."""
    screen = screeninfo.get_monitors()[0]  # Get primary screen
    return f"{screen.width}x{screen.height}"

def save_to_csv(filename="system_info.csv"):
    """Saves system details to a CSV file, replacing previous data."""
    uid = get_system_uid()
    specs = get_system_specs()
    resolution = get_screen_resolution()

    # Define the header and data
    headers = ["UID", "OS", "OS Version", "Processor", "RAM", "Screen Resolution"]
    data = [uid, specs["OS"], specs["OS Version"], specs["Processor"], specs["RAM"], resolution]

    # Write to CSV (overwrite mode)
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerow(data)

if __name__ == "__main__":
    save_to_csv()
    print("System info saved to 'system_info.csv'")
