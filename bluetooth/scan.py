#!/usr/bin/python3

# geektechstuff bluetooth
import bluetooth
import time

def scan(ctime):
    print("Scanning for bluetooth devices:",ctime)
    devices = bluetooth.discover_devices(lookup_names = True, lookup_class = True)
    number_of_devices = len(devices)
    print(number_of_devices,"devices found")

    for addr, name, device_class in devices:
        print("\n")
        print("Device:")
        print("Device Name: %s" % (name))
        print("Device MAC Address: %s" % (addr))
        print("Device Class: %s" % (device_class))
        print("\n")
    return

if __name__ == "__main__":
    while True:
        scan(time.monotonic())
        time.sleep(1.0)