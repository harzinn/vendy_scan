README for Vendor Lookup Tool
This Python script, vendor_lookup.py, is a tool for analyzing a pcap (Packet Capture) file to identify the MAC addresses of devices within the captured network traffic and retrieve their respective vendors using a public API. It then saves this information in a CSV file. This tool can be useful for network administrators and security professionals who want to gain insights into the types of devices present on a network.
Prerequisites
Before using this tool, ensure that you have the following prerequisites:
    1. Python: You need to have Python 3 installed on your system.
    2. Required Python Libraries: Make sure you have installed the necessary Python libraries using the following command:
pip install pyshark requests

README for Vendor Lookup Tool
This Python script, vendor_lookup.py, is a tool for analyzing a pcap (Packet Capture) file to identify the MAC addresses of devices within the captured network traffic and retrieve their respective vendors using a public API. It then saves this information in a CSV file. This tool can be useful for network administrators and security professionals who want to gain insights into the types of devices present on a network.
Prerequisites
Before using this tool, ensure that you have the following prerequisites:
    1. Python: You need to have Python 3 installed on your system.
    2. Required Python Libraries: Make sure you have installed the necessary Python libraries using the following command:
    1. pip install pyshark requests
Usage
To use the vendor_lookup.py script, follow these steps:
    1. Open a command prompt or terminal.
    2. Navigate to the directory containing the script using the cd command.
    3. Run the script with the following command:

python3 vendor_lookup.py <path_to_pcap_file>

Replace <path_to_pcap_file> with the path to the pcap file you want to analyze.
For example:
python3 vendor_lookup.py my_network_capture.pcap

    • he script will start processing the pcap file. It will send requests to an external API to retrieve vendor information for each MAC address it encounters in the pcap file. The results will be displayed in the terminal as they are fetched.
    • Once the analysis is complete, you will be prompted to save the results to a CSV file. A file dialog will appear, allowing you to choose the location and name of the output CSV file. By default, the file will have a .csv extension.
    • After selecting the output file location and name, the script will save the results to the CSV file and display a message indicating the operation's success.
    • If you choose not to select an output file, the script will cancel the operation and display a message accordingly.
Rate Limiting
The script includes a rate-limiting mechanism to prevent making too many API requests in a short period. The default delay between API requests is set to 1 second (API_REQUEST_DELAY). You can adjust this value in the script according to the API's rate limits or your needs.
Notes
    • The script uses the pyshark library to parse pcap files and extract MAC addresses from network packets.
    • It uses the requests library to fetch vendor information from the macvendors.com API.
    • If a MAC address is not found in the API database, it will be labeled as "Unknown."
    • The results are saved in a CSV file with two columns: "MAC Address" and "Vendor."
    • The tool provides a graphical file dialog for selecting the output file location and name.
License
This script is provided under an open-source license. You can find the license information in the source code.
Please use this tool responsibly and in compliance with any applicable laws and regulations.

