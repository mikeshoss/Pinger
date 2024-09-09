import os
import time
import json
import subprocess
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twilio credentials from .env
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
your_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
twilio_number = os.getenv('TWILIO_TWILIO_NUMBER')

# Create Twilio client
twilio_client = Client(account_sid, auth_token)

# Load machine details from JSON file
def load_machine_data():
    with open('machines.json', 'r') as file:
        return json.load(file)

# Load monitoring configuration from JSON file
def load_config_data():
    with open('config.json', 'r') as file:
        return json.load(file)

# Ping function to check if the IP is awake
def is_machine_awake(ip):
    response = os.system(f"ping -c 1 {ip} > /dev/null 2>&1")
    return response == 0

# Send Wake-On-LAN packet using etherwake and the correct port for each OS
def send_wol(mac, port):
    subprocess.call(['sudo', 'etherwake', '-i', 'eth0', mac])  # Replace eth0 with your network interface

# Send Twilio SMS notification with machine name and IP
def send_twilio_alert(machine_name, machine_ip, message_body):
    full_message = f"{machine_name} ({machine_ip}): {message_body}"
    message = twilio_client.messages.create(
        to=your_phone_number,
        from_=twilio_number,
        body=full_message
    )
    print(f"Twilio alert sent: {full_message}, SID: {message.sid}")

# Monitor all machines with state tracking for online/offline
def monitor_all_machines(machines, ports):
    machine_status = {machine['name']: 'online' for machine in machines.values()}  # Track machine status
    config_last_modified_time = os.path.getmtime('config.json')

    # Load the initial config
    config = load_config_data()

    while True:
        # Reload config data if config.json has been modified
        if os.path.getmtime('config.json') != config_last_modified_time:
            config = load_config_data()
            config_last_modified_time = os.path.getmtime('config.json')

        retries = config['retries']
        retry_interval = config['retry_interval']
        check_interval = config['check_interval']

        # Reload machine data from JSON file if modified
        machines = load_machine_data()['devices']

        for machine_name, machine in machines.items():
            print(f"Pinging {machine_name} ({machine['ip']})")

            if machine_status[machine_name] == 'offline':
                # If the machine is already marked as offline, just report it as offline
                if not is_machine_awake(machine['ip']):
                    print(f"{machine_name} ({machine['ip']}) is still offline.")
                else:
                    # If the machine is back online, report and reset the status
                    print(f"{machine_name} ({machine['ip']}) is back online.")
                    send_twilio_alert(machine_name, machine['ip'], "is back online.")
                    machine_status[machine_name] = 'online'
            else:
                # If machine is online, proceed with the ping check
                if is_machine_awake(machine['ip']):
                    print(f"{machine_name} ({machine['ip']}) is awake.")
                else:
                    print(f"{machine_name} ({machine['ip']}) is not responding. Retrying...")

                    # Retry 7 times every 5 seconds (or based on config)
                    for attempt in range(retries):
                        time.sleep(retry_interval)
                        if is_machine_awake(machine['ip']):
                            print(f"{machine_name} ({machine['ip']}) is now back online.")
                            break
                    else:
                        # If all retries fail, mark the machine as offline and send notification
                        print(f"{machine_name} ({machine['ip']}) failed to respond after {retries} retries. Sending WOL and Twilio alert.")
                        port = ports.get(machine['os'], 9)  # Default to port 9 if not found
                        send_wol(machine['mac'], port)
                        send_twilio_alert(machine_name, machine['ip'], "is offline.")
                        machine_status[machine_name] = 'offline'  # Mark as offline

        # Countdown until the next check
        for remaining_time in range(check_interval * 60, 0, -1):
            print(f"Next check in {remaining_time // 60} minutes and {remaining_time % 60} seconds", end='\r')
            time.sleep(1)  # Sleep for 1 second to update the countdown in real-time

if __name__ == '__main__':
    # Load machine data from the JSON file
    data = load_machine_data()

    # Extract ports and devices from the loaded JSON data
    ports = data['ports']
    machines = data['devices']

    # Start monitoring all machines
    monitor_all_machines(machines, ports)