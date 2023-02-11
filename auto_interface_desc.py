from netmiko import ConnectHandler
from cisco_cdp_neighbor import *
from getpass import getpass
# Step1:
# Get device credentials.
ip_address = input("IP address of the switch: ")
username = input("Username: ")
password = getpass("Password: ")
device = {"device_type": "cisco_ios", "host": ip_address, "username": username, "password": password}

# Step2:
# Connect to the device.
print(f"Connecting to {ip_address}...")
device_connect = ConnectHandler(**device)

# Step3:
# Get CDP neighbors in a dict format
print("Fetching cdp neighbors...")
cdp_neighbors = get_cdp_neighbors(device_connect.send_command("show cdp neighbor"))

# Step4:
# Change the description of the interface according to the cdp neighbor output
for interface, neighbor in cdp_neighbors.items():
    print(f"Modifying the description of interface {interface}...")
    neighbor_device = neighbor[0]["hostname"].strip()
    neighbor_port = neighbor[0]["port"].strip()
    config_set = [f"interface {interface}", f"description ***Connected to {neighbor_device} on {neighbor_port}***"]
    device_connect.send_config_set(config_commands=config_set)






