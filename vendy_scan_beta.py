import pyshark
import csv
import requests
import sys
import time

# Constants
API_REQUEST_DELAY = 1
PACKET_COUNT_INTERVAL = 15  # Interval for packet count

def get_vendor(mac_address):
    """Get vendor for a given MAC address with rate limiting."""
    try:
        url = f'https://api.macvendors.com/{mac_address}'
        response = requests.get(url)
        if response.status_code == 429:
            time.sleep(API_REQUEST_DELAY)
            return get_vendor(mac_address)
        return response.text if response.status_code == 200 else 'Unknown'
    except requests.RequestException:
        return 'Unknown'

def analyze_pcap(file_path):
    """Analyze pcap file and save known devices with their vendors."""
    cap = pyshark.FileCapture(file_path)
    known_devices = {}

    packet_processed = 0
    start_time = time.time()  # Start time for packet processing

    for packet in cap:
        packet_processed += 1
        try:
            mac_address = packet.eth.src
            if mac_address not in known_devices:
                vendor = get_vendor(mac_address)
                known_devices[mac_address] = vendor
                print(f"New MAC Address found: {mac_address}, Vendor: {vendor}")
            
            # Check if interval has passed to print packet count
            if time.time() - start_time >= PACKET_COUNT_INTERVAL:
                print(f"Total packets processed so far: {packet_processed}")
                start_time = time.time()  # Reset start time

        except AttributeError:
            continue

    output_results(known_devices)

def output_results(known_devices):
    """Output the results to a file."""
    output_file = select_output_file()
    if output_file:
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['MAC Address', 'Vendor']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for mac, vendor in known_devices.items():
                writer.writerow({'MAC Address': mac, 'Vendor': vendor})
        print(f'Analysis complete. Results saved to {output_file}')

def select_output_file():
    """Create a pop-up window for output file selection."""
    from tkinter import filedialog, Tk
    root = Tk()
    root.withdraw()
    return filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files", "*.csv")], title="Save the output file as")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 vendy_scan.py <path_to_pcap_file>")
    else:
        file_path = sys.argv[1]
        analyze_pcap(file_path)
