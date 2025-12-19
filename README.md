# 🛠️ Modbus Swiss Army Knife

**Modbus Swiss Army Knife** is an all-in-one offensive and defensive testing utility for **Modbus TCP** environments.  
It is designed for **OT/ICS cybersecurity professionals, penetration testers, and students** who want a practical way to **interact with, enumerate, manipulate, and analyze Modbus-enabled PLCs and devices**.

This tool intentionally exposes how **unauthenticated and insecure Modbus really is**—making it ideal for labs, training, tabletop exercises, and authorized security assessments.

---

## 🚨 Disclaimer

> **This tool is for educational and authorized security testing only.**  
>  
> Do **NOT** run this against systems you do not own or have explicit permission to test.  
> Modbus lacks authentication and safety controls—misuse can cause **process disruption, equipment damage, or safety incidents**.

By using this tool, you accept full responsibility for how it is used.

---

## ✨ Features

- 🔌 **Modbus TCP Client**
  - Connects to PLCs and Modbus devices over TCP/502
  - Supports configurable unit IDs

- 📖 **Read Operations**
  - Read coils
  - Read holding registers
  - Enumerate ranges of coils and registers

- ✍️ **Write Operations**
  - Write individual coils
  - Write individual registers
  - Flip coil values
  - Zero out coils (⚠️ intentionally dangerous)

- 🧠 **Device Intelligence**
  - Read Modbus Device Identification
  - Fingerprint vendor / device information when available

- 🧪 **Offensive Testing**
  - Register fuzzing
  - Mass state manipulation
  - Behavior observation under malformed or unexpected values

- 📡 **Traffic Capture**
  - Optional **PCAP / PCAPNG** capture of Modbus traffic
  - Useful for Wireshark analysis, blue-team detection labs, and training

- 🖥️ **Cross-Platform**
  - Windows
  - Linux
  - Kali Linux
  - Automatically detects loopback and active interfaces for capture

- 📋 **Interactive Menu**
  - Simple terminal-based interface
  - Designed for live demos and classroom use

---

## 🧩 Why This Tool Exists

Modbus is:
- ❌ Insecure by design
- ❌ Lacks authentication
- ❌ Lacks encryption
- ❌ Widely deployed in critical infrastructure

**Modbus Swiss Army Knife** exists to:
- Demonstrate **real-world OT/ICS risk**
- Support **hands-on learning**
- Enable **repeatable security testing**
- Bridge the gap between **theory and reality**

---

## 📦 Installation

### Prerequisites

- Python **3.8+**
- Network access to a Modbus TCP device or simulator
- Administrative privileges (required for packet capture)

### Install Dependencies

```bash
pip install pymodbus scapy psutil netifaces
