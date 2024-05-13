from flask import Flask, request, jsonify
import json
import smtplib  # For email notifications

app = Flask(__name__)
device_status = {}
config = {}

def send_notification(email, message):
    # Placeholder for email notification logic
    # You would need to configure SMTP settings and possibly use a library like smtplib
    print(f"Sending email to {email} with message: {message}")

@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    slave_id = request.args.get('slave_id')
    if slave_id in config['Pingers']:
        return jsonify([device for device in config['Devices'] if device['ping_group'] == slave_id])
    else:
        return jsonify({"error": "Slave not found"}), 404

@app.route('/report', methods=['POST'])
def report():
    data = request.json
    device_status[data['name']] = data['status']
    device_config = next((device for device in config['Devices'] if device['name'] == data['name']), None)
    if device_config and 'notifications' in device_config:
        send_notification(device_config['notifications']['email'], f"{data['name']} is {data['status']}")
    return "Status updated"

@app.route('/status')
def status():
    return jsonify(device_status)

def load_config():
    with open('config.json', 'r') as f:
        global config
        config = json.load(f)

if __name__ == '__main__':
    load_config()
    app.run(host='0.0.0.0', port=8080)
