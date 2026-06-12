# Pinger

A Python network monitoring tool that watches device health across one or more sites, sends Wake-On-LAN packets to revive unresponsive machines, and alerts you by SMS when devices go offline or come back online.

## Features

- Periodically pings a configurable list of devices to check whether they are responding.
- Per-device retry logic: when a device stops responding, it is retried a configurable number of times before being declared offline.
- Sends a Wake-On-LAN (WOL) packet via `etherwake` to attempt to wake an offline machine, using an OS-specific WOL port.
- Sends SMS alerts through [Twilio](https://www.twilio.com/) when a device goes offline and again when it comes back online.
- State tracking so you receive a single offline alert per outage (not on every check) and a recovery alert when the device returns.
- Hot-reloads its configuration and device list on each cycle: edits to the config and machine files are picked up without restarting the process.
- Configurable retry count, retry interval, and check interval.

## Requirements

- Python 3
- Python packages:
  - [`twilio`](https://pypi.org/project/twilio/) — for sending SMS alerts
  - [`python-dotenv`](https://pypi.org/project/python-dotenv/) — for loading credentials from a `.env` file
- [`etherwake`](https://manpages.debian.org/etherwake) installed and available on the host (used to send Wake-On-LAN packets). The script invokes it with `sudo`.
- A network interface that supports Wake-On-LAN. The script is configured for `eth0` by default (see Configuration).
- A [Twilio](https://www.twilio.com/) account with an SMS-capable phone number.

Install the Python dependencies with:

```bash
pip install twilio python-dotenv
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mikeshoss/Pinger.git
   cd Pinger
   ```

2. Install the Python dependencies:

   ```bash
   pip install twilio python-dotenv
   ```

3. Ensure `etherwake` is installed on the host that will run Pinger (for example, on Debian/Ubuntu: `sudo apt-get install etherwake`).

## Configuration

Pinger reads three files at runtime. The repository ships example/template versions you should copy and edit.

### 1. Twilio credentials (`.env`)

Copy `env.txt` to `.env` and fill in your Twilio credentials:

```bash
cp env.txt .env
```

`.env` contents:

```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=the_number_alerts_are_sent_to
TWILIO_TWILIO_NUMBER=your_twilio_sending_number
```

- `TWILIO_PHONE_NUMBER` is the destination number that receives the alerts.
- `TWILIO_TWILIO_NUMBER` is your Twilio number that the messages are sent from.

`.env` is git-ignored so your credentials are not committed.

### 2. Devices (`machines.json`)

The script loads device definitions from `machines.json`. Use `machines-example.json` as a starting template:

```bash
cp machines-example.json machines.json
```

The file has two top-level keys, `ports` and `devices`:

```json
{
    "ports": {
        "macOS": 9,
        "Linux": 7,
        "Windows": 7
    },
    "devices": {
        "Device1": {
            "name": "Device1",
            "ip": "192.168.1.10",
            "mac": "AA:BB:CC:DD:EE:FF",
            "os": "macOS"
        }
    }
}
```

- `ports` maps an operating-system name to the Wake-On-LAN port used for devices of that OS. If a device's OS is not found in this map, port `9` is used as the default.
- `devices` is a map of device entries. For each device set:
  - `name` — a human-readable name used in log output and alerts.
  - `ip` — the IP address to ping.
  - `mac` — the MAC address used for the Wake-On-LAN packet.
  - `os` — the operating system, used to look up the WOL port from the `ports` map.

You can list as many devices as you like; to monitor multiple sites, simply include all of their devices in this file. `machines.json` is git-ignored.

### 3. Monitoring settings (`config.json`)

The script loads timing settings from `config.json`. The repository includes a template named `conflig.json`; copy it to `config.json`:

```bash
cp conflig.json config.json
```

Contents:

```json
{
    "retries": 7,
    "retry_interval": 5,
    "check_interval": 5
}
```

- `retries` — number of additional ping attempts before a device is declared offline.
- `retry_interval` — seconds to wait between retry attempts.
- `check_interval` — minutes to wait between full monitoring cycles.

`config.json` is hot-reloaded: if you edit it while Pinger is running, the new values are applied on the next cycle.

### Network interface

Wake-On-LAN packets are sent over the `eth0` interface by default. If your host uses a different interface, update the interface name in the `send_wol` function in `ping_and_wol_all.py`.

## Usage

After creating `.env`, `machines.json`, and `config.json`, run:

```bash
python ping_and_wol_all.py
```

Because the script calls `etherwake` via `sudo`, you may need to run it with privileges that allow `sudo etherwake` without an interactive password prompt for unattended operation.

While running, Pinger will:

1. Ping each device in `machines.json`.
2. Retry any non-responding device up to `retries` times, `retry_interval` seconds apart.
3. If a device stays unresponsive, send a Wake-On-LAN packet, send a Twilio "is offline" SMS, and mark it offline.
4. When an offline device responds again, send a Twilio "is back online" SMS and mark it online.
5. Wait `check_interval` minutes (with a live countdown printed to the console) before the next cycle.

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) and [NOTICE](NOTICE) files for details.
