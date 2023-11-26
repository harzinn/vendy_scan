import pyshark
import csv
import requests
import time
import sys
import tkinter as tk
from tkinter import filedialog

# Define a delay in seconds between API requests
API_REQUEST_DELAY = 1  # Adjust this value as needed

def get_vendor(mac_address):
    """Get the vendor for a given MAC address with rate limiting."""
    try:
        url = f'https://api.macvendors.com/{mac_address}'
        response = requests.get(url)
        
        # Check if the response status code is 429 (Too Many Requests)
        if response.status_code == 429:
            time.sleep(API_REQUEST_DELAY)  # Wait before retrying
            return get_vendor(mac_address)  # Retry the request
        
        if response.status_code == 200:
            vendor = response.text
            return vendor
        else:
            return 'Unknown'
    except requests.RequestException:
        return 'Unknown'

def analyze_pcap(file_path):
    """Analyze the pcap file and save known devices with their vendors."""
    cap = pyshark.FileCapture(file_path)
    known_devices = {}

    for packet in cap:
        try:
            mac_address = packet.eth.src
            if mac_address not in known_devices:
                vendor = get_vendor(mac_address)
                known_devices[mac_address] = vendor
                if vendor != 'Unknown':
                    print(f'Fetched vendor for MAC Address: {mac_address}, Vendor: {vendor}')
        except AttributeError:
            continue

    output_file = select_output_file()
    if output_file:
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['MAC Address', 'Vendor']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for mac, vendor in known_devices.items():
                writer.writerow({'MAC Address': mac, 'Vendor': vendor})

        print(f'Analysis complete. Results saved to {output_file}')
    else:
        print('No output file selected. Operation cancelled.')

def select_output_file():
    """Create a pop-up window for the user to select a location and name for the output file."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files", "*.csv")], title="Save the output file as")
    return file_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 vendy_scan.py <path_to_pcap_file>")
    else:
        file_path = sys.argv[1]
        analyze_pcap(file_path)
