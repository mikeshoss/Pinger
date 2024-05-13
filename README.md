## Pinger: Raspberry Pi Network Monitoring System

### Description
This project is designed to monitor the health and status of network devices using a network of Raspberry Pis. It utilizes Tailscale for secure communication between remote and local devices, providing a centralized dashboard to view the status of all monitored devices.

### Features
- **Device Monitoring:** Regular pings to check device availability.
- **Dynamic Configuration:** Utilizes Tailscale API to automatically update device configurations.
- **Web Interface:** Provides a real-time status dashboard accessible via a web browser.
- **Notifications:** Sends alerts for device status changes.

### Prerequisites
Before you begin, ensure you have the following:
- Raspberry Pi devices (with Raspbian OS installed).
- Internet connection for each Raspberry Pi.
- Tailscale installed on each Raspberry Pi ([Installation Guide](https://tailscale.com/kb/1101/install-rpi/)).
- Python 3.x installed on each Raspberry Pi.

### Installation
1. **Clone the Repository**
   ```
   git clone https://github.com/mikeshoss/Pinger.git
   cd pinger
   ```

2. **Install Required Python Packages**
   ```
   pip install -r requirements.txt
   ```

3. **Setup Tailscale**
   - Follow the instructions on the Tailscale website to connect each Raspberry Pi to your Tailnet.

4. **API Key Configuration**
   - Generate an API key from the Tailscale admin console with read access.
   - Set this key as an environment variable or store it securely for the application to use.

### Configuration
1. **API Key**
   - Store your Tailscale API key in a secure location or environment variable.

2. **Modify `config.json.example`**
   - Rename `config.json.example` to `config.json`.
   - Update the configuration according to your network setup.

### Usage
- **Starting the Master Node Server**
  ```
  python master.py
  ```
- **Running Slave Nodes**
  ```
  python slave.py
  ```
- **Accessing the Dashboard**
  - Open a web browser and navigate to `http://[master-ip-address]:8080/status` to view the network status dashboard.

### Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### License
Distributed under the MIT License. See `LICENSE` for more information.

### Contact
Your Name - mike.shoss@gmail.com

Project Link: [https://github.com/mikeshoss/Pinger](https://github.com/mikeshoss/Pinger)

---

### Additional Notes:
- **Security**: Ensure all communication is secured and sensitive data is encrypted as needed.
- **Updates**: Regularly update the system to handle new security patches for Raspberry Pi and Python dependencies.
