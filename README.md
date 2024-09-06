# Pinger

This Python script is designed to monitor the status of multiple machines and send Wake-On-LAN (WOL) packets if they are not responding. The script pulls machine details from a JSON file and checks their IP addresses for responsiveness. If a machine is not responding after a specified number of retries, the script sends a WOL packet to wake it up.

## Installation:

1. Create a directory for the project.
2. Copy the `machines-example.json` and `ping_and_wol_all.py` files into the directory.
3. Rename `machines-example.json` to `machines.json`
4. Populate the `machines.json` with your device information.
5. Run the script using the command `python ping_and_wol_all.py`.

## Usage:

* The `machines.json` file contains a list of machines and their details, including name, IP address, MAC address, and operating system.
* The `ports` dictionary in the JSON file specifies the port for sending WOL packets for each operating system.
* The script will continuously monitor the machines and send WOL packets if necessary.

## Features:

* Pulls the latest machine details from the JSON file.
* Checks for modified JSON files and reloads data accordingly.
* Sends WOL packets to unresponsive machines.
* Configurable number of retries before sending WOL packets.
* Configurable interval for monitoring.

## Benefits:

* Automated monitoring of machine status.
* Prompt notification of unresponsive machines.
* Convenience and ease of use.

## Usage Notes:

* Ensure that the IP addresses in the JSON file are correct.
* The script requires root privileges to send WOL packets.
* The port numbers in the JSON file may vary depending on the specific hardware and configuration.
