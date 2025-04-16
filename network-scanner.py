import socket
import re
import sys
from requests import get

# Function to validate IP address
def is_valid_ip(ip):
    # Regular expression for IPv4 address format validation
    ip_pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
    match = re.match(ip_pattern, ip)
    
    if not match:
        return False
    
    # Check if each octet is in range 0-255
    for i in range(1, 5):
        octet = int(match.group(i))
        if octet < 0 or octet > 255:
            return False
    
    return True

# Function to validate port number
def is_valid_port(port):
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except ValueError:
        return False

# Check If Port Is Open
def isOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        with open("rzlt.txt", "a+") as file:
            file.write(ip)
            file.write("\n +++++++++++++++++++++++++++++ Code from R3DHULK +++++++++++++++++++++++++++++\n")
        print(ip, "Is up")
    except socket.timeout:
        print(f"{ip} - Connection timed out")
    except ConnectionRefusedError:
        print(f"{ip} - Connection refused")
    except Exception as e:
        print(f"{ip} - Is Down: {str(e)}")
    finally:
        s.close()

# Range Ip Function ipRange
def ipRange(start_ip, end_ip):
    if not is_valid_ip(start_ip) or not is_valid_ip(end_ip):
        print("Error: Invalid IP address format.")
        return []
    
    # Convert IP addresses to integers for comparison
    def ip_to_int(ip):
        octets = list(map(int, ip.split('.')))
        return (octets[0] << 24) + (octets[1] << 16) + (octets[2] << 8) + octets[3]
    
    start_int = ip_to_int(start_ip)
    end_int = ip_to_int(end_ip)
    
    if start_int > end_int:
        print("Error: Start IP is greater than End IP.")
        return []
    
    if end_int - start_int > 1000:
        proceed = input("Warning: You are about to scan more than 1000 IPs. Continue? (y/n): ")
        if proceed.lower() != 'y':
            return []
    
    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    temp = start.copy()
    ip_range = []
    ip_range.append(start_ip)
    
    while temp != end:
        temp[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i-1] += 1
        ip_range.append(".".join(map(str, temp)))
    
    return ip_range

# logo
print('''
**********************************************************************
* _ _ _ _ ___ *
* | \| |___| |___ __ _____ _ _| |__ / __| __ __ _ _ _ _ _ ___ _ _ *
* | .` / -_) _\ V V / _ \ '_| / / \__ \/ _/ _` | ' \| ' \/ -_) '_| *
* |_|\_\___|\__|\_/\_/\___/_| |_\_\ |___/\__\__,_|_||_|_||_\___|_| *
* *
* code from R3dHULK *
* github page : https://github.com/R3DHULK *
* *
**********************************************************************
''')

# Get valid IP input with validation
def get_valid_ip_input(prompt):
    while True:
        ip = input(prompt)
        if is_valid_ip(ip):
            return ip
        print("Error: Invalid IP address format. Example: 192.168.1.1")

# Get valid port input with validation
def get_valid_port_input():
    while True:
        port = input("Put Port To Check if It is Up: ")
        if is_valid_port(port):
            return port
        print("Error: Invalid port number. Please enter a value between 1-65535.")

# Main program
try:
    From = get_valid_ip_input("Put Start From Range: ")
    To = get_valid_ip_input("Put End Of Range: ")
    
    ip_range = ipRange(From, To)
    if not ip_range:
        print("There was a problem with the IP range. Exiting program.")
        sys.exit(1)
    
    port = get_valid_port_input()
    
    print("Starting scan from", From, "to", To)
    
    try:
        External_IP = get('https://api.ipify.org').text  # get External Ip
        print("Your external IP is:", External_IP)
    except Exception as e:
        print("Failed to retrieve external IP:", str(e))
    
    ok = input("Press Enter To Start ")
    print(" ")
    print("*** Starting scan *** ")
    print(" ")
    
    for ip in ip_range:
        print("Checking", ip)
        isOpen(ip, port)
    
    input("Press Enter To Exit")

except KeyboardInterrupt:
    print("\nProgram interrupted by user.")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
