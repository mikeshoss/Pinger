import requests
import json
from pythonping import ping
import time

def ping_device(ip_address):
    response = ping(ip_address, count=4)
    return response.success()

def report_status(master_ip, master_port, device_name, status):
    url = f"http://{master_ip}:{master_port}/report"
    data = {'name': device_name, 'status': status}
    requests.post(url, json=data)

def get_tasks(master_ip, master_port, slave_id):
    url = f"http://{master_ip}:{master_port}/get_tasks?slave_id={slave_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

if __name__ == '__main__':
    master_ip = '192.168.1.100'  # IP of the master device
    master_port = '8080'
    slave_id = 'Slave1'  # Unique identifier for each slave

    while True:
        tasks = get_tasks(master_ip, master_port, slave_id)
        for device in tasks:
            is_up = ping_device(device['ip'])
            report_status(master_ip, master_port, device['name'], 'Online' if is_up else 'Offline')
            time.sleep(device.get('ping_interval', 10))  # Use specific interval or default to 10 seconds
