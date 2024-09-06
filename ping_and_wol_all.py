import os
import time
import json
import subprocess

# Load machine details from JSON file
def load_machine_data():
    with open('machines.json', 'r') as file:
        return json.load(file)

# Ping function to check if the IP is awake
def is_machine_awake(ip):
    response = os.system(f"ping -c 1 {ip} > /dev/null 2>&1")
    return response == 0

# Send Wake-On-LAN packet using etherwake and the correct port for each OS
def send_wol(mac, port):
    subprocess.call(['sudo', 'etherwake', '-i', 'eth0', mac])  # Replace eth0 with your network interface

def monitor_all_machines(machines, ports, retries, interval):
    failure_counts = {machine['name']: 0 for machine in machines.values()}

    while True:
        # Check for updated JSON file
        if os.path.getmtime('machines.json') > os.path.getmtime(os.path.basename(__file__)):
            # Reload machine data if the JSON file has been modified
            machines = load_machine_data()['devices']

        for machine_name, machine in machines.items():
            print(f"Pinging {machine_name} ({machine['ip']})")

            if is_machine_awake(machine['ip']):
                print(f"{machine_name} is awake")
                failure_counts[machine_name] = 0  # Reset failure count if machine responds
            else:
                print(f"{machine_name} is not responding")
                failure_counts[machine_name] += 1
                if failure_counts[machine_name] >= retries:
                    # Look up the port based on the OS
                    port = ports.get(machine['os'], 9)  # Default to 9 if not found
                    print(f"Sending WOL to {machine_name} (MAC: {machine['mac']}, Port: {port})")
                    send_wol(machine['mac'], port)
                    failure_counts[machine_name] = 0  # Reset after sending WOL

        # Wait for the interval before pinging again
        time.sleep(interval * 60)

if __name__ == '__main__':
    # Load the machine data from the JSON file
    data = load_machine_data()

    # Extract ports and devices from the loaded JSON data
    ports = data['ports']
    machines = data['devices']

    # Monitoring configuration
    retries = 10  # Number of times to retry before sending WOL
    interval = 5  # Interval in minutes

    # Monitor all machines
    monitor_all_machines(machines, ports, retries, interval)