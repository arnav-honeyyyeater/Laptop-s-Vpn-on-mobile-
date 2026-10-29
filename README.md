# 🌐 Laptop's VPN on Mobile

> Share your laptop's active VPN connection with your mobile phone (Android / iOS) over Windows Mobile Hotspot — without needing VPN apps or extra subscriptions on your phone!

---

## 💡 The Problem

When you turn on a VPN on your Windows laptop and enable **Mobile Hotspot**, Windows default routing does **not** route connected hotspot devices through the VPN adapter. Devices connected to your hotspot end up using your unencrypted, regular ISP connection.

## 🛠️ The Solution

This lightweight, zero-dependency Python proxy runs on your laptop. By setting your phone's Wi-Fi proxy to point to your laptop's hotspot IP address, all HTTP and HTTPS traffic from your phone is tunneled through your laptop's active VPN connection.

```
┌─────────────────┐       Wi-Fi       ┌──────────────────────────────────────────────┐
│  Mobile Device  │ ────────────────> │               Windows Laptop                 │
│ (Android / iOS) │   Proxy: 8080     │                                              │
└─────────────────┘                   │  ┌──────────────────┐   ┌─────────────────┐  │
                                      │  │ proxy_router.py  │──>│   Active VPN    │  │
                                      │  │ (192.168.137.1)  │   │     Tunnel      │  │
                                      │  └──────────────────┘   └────────┬────────┘  │
                                      └──────────────────────────────────┼───────────┘
                                                                         │
                                                                         ▼
                                                                🔒 Encrypted Internet
```

---

## ✨ Features

- **Zero External Dependencies**: Uses only standard Python libraries (`socket`, `select`, `threading`). No `pip install` required!
- **Encrypted HTTPS Support**: Full HTTP `CONNECT` tunneling for SSL/TLS encrypted traffic.
- **1-Click Starter**: Just double-click `Start-VPN-Hotspot-Proxy.bat`.
- **Universal Compatibility**: Works with **Android**, **iOS (iPhone/iPad)**, or any device connected to your hotspot.
- **Works with Any VPN**: Compatible with NordVPN, ExpressVPN, Surfshark, Cloudflare WARP, ProtonVPN, OpenVPN, WireGuard, corporate VPNs, etc.

---

## 📋 Prerequisites

1. **Windows 10 or 11** with Wi-Fi Hotspot capability.
2. **Python 3.x** installed ([Download Python](https://www.python.org/downloads/) — make sure to check *"Add Python to PATH"* during installation).
3. Any active VPN connected on your laptop.

---

## 🚀 Quick Start Guide

### Step 1: Connect your Laptop to your VPN
Open your VPN client on your laptop (e.g., NordVPN, ExpressVPN, WARP) and connect to your preferred server location.

---

### Step 2: Turn on Windows Mobile Hotspot
1. On your Windows laptop, open **Settings** (`Win + I`).
2. Go to **Network & internet** > **Mobile hotspot**.
3. Toggle Mobile hotspot to **On**.
4. Note your hotspot's Network name (SSID) and Password.

---

### Step 3: Start the Proxy Server
Double-click:
```text
Start-VPN-Hotspot-Proxy.bat
```
*(Or open a terminal in this folder and run `python proxy_router.py`)*

You will see:
```text
============================================================
        Hotspot VPN Proxy Server for Mobile Phone
============================================================

Hotspot IP : 192.168.137.1
Proxy Port : 8080

[+] Hotspot VPN Proxy Server listening on 0.0.0.0:8080...
```
> ⚠️ **Keep this window open** while using the proxy on your phone.

---

### Step 4: Connect your Phone and Configure the Proxy

Connect your phone to the laptop's Mobile Hotspot Wi-Fi network, then configure manual proxy settings:

<details>
<summary><b>📱 For Android</b></summary>

1. Open **Settings** > **Wi-Fi / Network**.
2. Tap the **Settings gear ⚙️** next to your laptop's hotspot network (or long-press the network name and select **Modify network**).
3. Tap **Advanced options** (or expand details).
4. Find **Proxy** and change it from *None* to **Manual**.
5. Enter the following details:
   - **Proxy hostname**: `192.168.137.1`
   - **Proxy port**: `8080`
   - **Bypass proxy for**: *(leave empty or default)*
6. Tap **Save**.
</details>

<details>
<summary><b>🍎 For iPhone / iPad (iOS)</b></summary>

1. Open **Settings** > **Wi-Fi**.
2. Tap the blue **(i)** info icon next to your laptop's hotspot network.
3. Scroll down to the bottom to **HTTP PROXY**.
4. Tap **Configure Proxy** and choose **Manual**.
5. Enter the following details:
   - **Server**: `192.168.137.1`
   - **Port**: `8080`
   - **Authentication**: Off
6. Tap **Save** in the top-right corner.
</details>

---

### Step 5: Verify Connection ✅

On your phone:
1. Open any browser.
2. Visit [https://whatismyipaddress.com](https://whatismyipaddress.com) or [https://ipinfo.io](https://ipinfo.io).
3. You should see the IP address and location of your **laptop's VPN**!

---

## 🛑 Disconnecting (When Done)

1. On your phone, go back to Wi-Fi settings and set **Proxy** back to **None** (or **Off**).
2. Close the command prompt window on your laptop running the proxy.
3. Turn off Mobile Hotspot if you no longer need it.

---

## ❓ Troubleshooting

<details>
<summary><b>1. Phone says "No Internet connection" or pages don't load</b></summary>

- **Windows Firewall**: Windows Firewall may be blocking incoming connections to port 8080.
  - When prompted by Windows Defender Firewall, check both **Private** and **Public** networks and click **Allow access**.
  - Alternatively, allow Python through the Windows Firewall:
    - *Control Panel > Windows Defender Firewall > Allow an app or feature through Windows Defender Firewall > Find Python > Check both Private and Public*.
- **Check Hotspot IP Address**: By default, Windows sets the hotspot adapter to `192.168.137.1`. If yours is different:
  1. Open Command Prompt on your laptop.
  2. Run `ipconfig`.
  3. Look for the adapter named `Local Area Connection*` or `Wi-Fi (Microsoft Wi-Fi Direct Virtual Adapter)`.
  4. Use the `IPv4 Address` listed under that adapter as your proxy host.
</details>

<details>
<summary><b>2. Some apps on mobile don't route through proxy</b></summary>

- Standard web browsers (Chrome, Safari, Firefox), YouTube, and most apps respect the system Wi-Fi proxy settings.
- A few apps that ignore system proxy settings or use non-HTTP/HTTPS protocols (like raw UDP or proprietary sockets, Like some games) will not route through an HTTP proxy.
</details>

<details>
<summary><b>3. 'python' is not recognized as an internal or external command</b></summary>

- You need to add Python to your system PATH:
  - Re-run the Python installer, select **Modify**, and make sure **Add Python to environment variables** is checked.
</details>

---

## 📁 Repository Structure

```text
├── .gitignore
├── README.md
├── Start-VPN-Hotspot-Proxy.bat   # 1-Click launcher script for Windows
└── proxy_router.py               # Pure Python HTTP/HTTPS proxy server
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
