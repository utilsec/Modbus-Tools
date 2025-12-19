#!/usr/bin/env python3
"""
============================================================
Modbus Utility Tool (v0.2.2)

This script was vibe coded by Mike Holcomb of UtilSec, LLC.

LinkedIn : https://www.linkedin.com/in/mikeholcomb
Website  : https://mikeholcomb.com
============================================================
"""

import sys
import os
import random
import argparse
from datetime import datetime
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

MAX_LENGTH = 1000
LOG_FILE = None

# ------------------------ Output & Logging ------------------------

def echo(msg):
    """User-facing output only"""
    print(msg)

def log(msg):
    """File-only logging"""
    if not LOG_FILE:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")

# ------------------------ Connection ------------------------

def connect_to_modbus(ip, port=502, readonly=False):
    client = ModbusTcpClient(ip, port=port)
    if client.connect():
        echo(f"[✓] Connected to Modbus service at {ip}:{port}")
        log(f"CONNECTED {ip}:{port}")
        if readonly:
            echo("[!] Read-Only Mode ENABLED")
            log("READ_ONLY_MODE ENABLED")
        return client
    else:
        echo("[✗] Failed to connect to Modbus service")
        log(f"FAILED_CONNECT {ip}:{port}")
        return None

# ------------------------ Coil Functions ------------------------

def read_coils(client):
    address = int(input("Enter starting coil address: "))
    count = int(input("Enter number of coils to read: "))

    log(f"READ_COILS addr={address} count={count}")
    result = client.read_coils(address, count)

    if result.isError():
        echo("Failed to read coils.")
        log("ERROR read_coils")
        return

    for i, val in enumerate(result.bits[:count]):
        echo(f"Coil[{address + i}] = {int(val)}")
        log(f"Coil[{address + i}] = {int(val)}")

def write_coil(client, readonly):
    if readonly:
        echo("Write blocked: Read-only mode.")
        log("WRITE_COIL blocked")
        return

    address = int(input("Enter coil address: "))
    value = int(input("Enter value (0 or 1): "))

    log(f"WRITE_COIL addr={address} value={value}")
    result = client.write_coil(address, bool(value))

    if result.isError():
        echo("Failed to write coil.")
        log("ERROR write_coil")
    else:
        echo(f"Coil[{address}] set to {value}")
        log("WRITE_SUCCESS")

# ------------------------ Register Functions ------------------------

def read_registers(client):
    address = int(input("Enter starting register address: "))
    count = int(input("Enter number of registers to read: "))

    log(f"READ_REGISTERS addr={address} count={count}")
    result = client.read_holding_registers(address, count)

    if result.isError():
        echo("Failed to read registers.")
        log("ERROR read_registers")
        return

    for i, val in enumerate(result.registers):
        echo(f"Register[{address + i}] = {val}")
        log(f"Register[{address + i}] = {val}")

def write_register(client, readonly):
    if readonly:
        echo("Write blocked: Read-only mode.")
        log("WRITE_REGISTER blocked")
        return

    address = int(input("Enter register address: "))
    value = int(input("Enter value (0-65535): "))

    log(f"WRITE_REGISTER addr={address} value={value}")
    result = client.write_register(address, value)

    if result.isError():
        echo("Failed to write register.")
        log("ERROR write_register")
    else:
        echo(f"Register[{address}] set to {value}")
        log("WRITE_SUCCESS")

# ------------------------ Scanning ------------------------

def scan_coils(client):
    echo("Scanning for coils...")
    log("SCAN_COILS started")
    found = 0

    for i in range(MAX_LENGTH):
        if not client.read_coils(i, 1).isError():
            found += 1
        else:
            break

    echo(f"Discovered {found} coils.")
    log(f"SCAN_COILS completed found={found}")

def scan_registers(client):
    echo("Scanning for registers...")
    log("SCAN_REGISTERS started")
    found = 0

    for i in range(MAX_LENGTH):
        if not client.read_holding_registers(i, 1).isError():
            found += 1
        else:
            break

    echo(f"Discovered {found} registers.")
    log(f"SCAN_REGISTERS completed found={found}")

# ------------------------ Device Identity ------------------------

def read_device_identity(client):
    echo("Reading device identity...")
    log("READ_DEVICE_IDENTITY")

    result = client.read_device_information()
    if result.isError():
        echo("Failed to retrieve device identity.")
        log("ERROR read_device_identity")
        return

    identity_map = {
        0x00: "VendorName",
        0x01: "ProductCode",
        0x02: "MajorMinorRevision",
        0x05: "ModelName",
        0x0A: "ProductName"
    }

    for obj_id, label in identity_map.items():
        value = result.information.get(obj_id, b"").decode(errors="ignore")
        echo(f"{label}: {value}")
        log(f"{label}: {value}")

# ------------------------ Advanced Actions ------------------------

def flip_all_coils(client, readonly):
    if readonly:
        echo("Flip blocked: Read-only mode.")
        log("FLIP_COILS blocked")
        return

    echo("Flipping all available coils...")
    log("FLIP_COILS started")
    count = 0

    for i in range(MAX_LENGTH):
        if not client.read_coils(i, 1).isError():
            count += 1
        else:
            break

    result = client.read_coils(0, count)
    if result.isError():
        echo("Failed to read coils.")
        log("ERROR flip_read")
        return

    for i, val in enumerate(result.bits[:count]):
        client.write_coil(i, not val)

    echo(f"Flipped {count} coils.")
    log(f"FLIP_COILS completed count={count}")

def zero_all_coils(client, readonly):
    if readonly:
        echo("Zeroing blocked: Read-only mode.")
        log("ZERO_COILS blocked")
        return

    echo("Zeroing all available coils...")
    log("ZERO_COILS started")
    count = 0

    for i in range(MAX_LENGTH):
        if not client.read_coils(i, 1).isError():
            count += 1
        else:
            break

    for i in range(count):
        client.write_coil(i, False)

    echo(f"Zeroed {count} coils.")
    log(f"ZERO_COILS completed count={count}")

def fuzz_registers(client, readonly):
    if readonly:
        echo("Fuzzing blocked: Read-only mode.")
        log("FUZZ_REGISTERS blocked")
        return

    echo("Fuzzing holding registers...")
    log("FUZZ_REGISTERS started")
    count = 0

    for i in range(MAX_LENGTH):
        if not client.read_holding_registers(i, 1).isError():
            count += 1
        else:
            break

    for i in range(count):
        value = random.randint(0, 65535)
        result = client.write_register(i, value)
        if not result.isError():
            log(f"Register[{i}] fuzzed value={value}")

    echo(f"Fuzzed {count} registers.")
    log(f"FUZZ_REGISTERS completed count={count}")

# ------------------------ Log Viewer ------------------------

def view_log():
    if not LOG_FILE or not os.path.exists(LOG_FILE):
        echo("Logging is not enabled or log file not found.")
        return

    echo("\n--- Current Log File ---")
    with open(LOG_FILE, "r") as f:
        print(f.read())
    echo("--- End of Log ---")

# ------------------------ Menu ------------------------

def show_menu(client, readonly):
    while True:
        print("\n--- Modbus Utility Menu ---")
        print("1.  Read Coils")
        print("2.  Write Coil")
        print("3.  Read Registers")
        print("4.  Write Register")
        print("5.  Scan for Coils")
        print("6.  Scan for Registers")
        print("7.  Read Device Identity")
        print("8.  Flip Coils")
        print("9.  Zero All Coils")
        print("10. Fuzz Registers")
        print("11. View Log File")
        print("12. Exit")

        choice = input("Select an option: ")

        try:
            if choice == "1":
                read_coils(client)
            elif choice == "2":
                write_coil(client, readonly)
            elif choice == "3":
                read_registers(client)
            elif choice == "4":
                write_register(client, readonly)
            elif choice == "5":
                scan_coils(client)
            elif choice == "6":
                scan_registers(client)
            elif choice == "7":
                read_device_identity(client)
            elif choice == "8":
                flip_all_coils(client, readonly)
            elif choice == "9":
                zero_all_coils(client, readonly)
            elif choice == "10":
                fuzz_registers(client, readonly)
            elif choice == "11":
                view_log()
            elif choice == "12":
                log("SESSION_END")
                break
            else:
                echo("Invalid option.")
        except (ValueError, ModbusException) as e:
            echo("Operation failed.")
            log(f"ERROR {e}")

# ------------------------ Main ------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modbus Utility Tool")
    parser.add_argument("ip", help="Target Modbus TCP IP address")
    parser.add_argument("--readonly", action="store_true", help="Enable read-only mode")
    parser.add_argument("--log", action="store_true", help="Enable file logging")
    args = parser.parse_args()

    if args.log:
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        LOG_FILE = f"modbus_log_{ts}.log"
        log("LOGGING_ENABLED")

    client = connect_to_modbus(args.ip, readonly=args.readonly)

    if client:
        try:
            show_menu(client, args.readonly)
        finally:
            client.close()
            log("DISCONNECTED")
