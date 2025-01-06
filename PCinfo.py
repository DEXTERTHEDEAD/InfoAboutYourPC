import os
import platform
import socket
import requests
import psutil
import subprocess
import re

def get_system_info():
    # Create a dictionary to store system information
    system_info = {
        'System': platform.system(),  # System type
        'Node Name': platform.node(),  # Node name
        'Release': platform.release(),  # Release
        'Version': platform.version(),  # Version
        'Machine': platform.machine(),  # Machine
        'Processor': platform.processor(),  # Processor
        'CPU Cores': os.cpu_count(),  # Number of cores
        'Memory': f"{round(psutil.virtual_memory().total / (1024.0 ** 3), 2)} GB",  # Memory size
        'Local IP Address': socket.gethostbyname(socket.gethostname()),  # Local IP address
        'Public IP Address': requests.get('https://api.ipify.org').text,  # Public IP address
        'Root Privileges': os.geteuid() == 0,  # Root privileges
        'Admin Privileges': 'Administrator' in subprocess.check_output('whoami', shell=True).decode('utf-8'),  # Admin privileges
        'Video Card': get_video_card_info(),  # Video card information
        'Disk Space': f"{round(psutil.disk_usage('/').free / (1024.0 ** 3), 2)} GB"  # Free disk space
    }
    return system_info

def get_video_card_info():
    # Get video card information based on the operating system
    if platform.system() == 'Windows':
        gpu_info = subprocess.check_output('wmic path win32_VideoController get name, AdapterRAM', shell=True).decode('utf-8')
        match = re.search(r'(\d+)MB', gpu_info)
        if match:
            return f"{int(match.group(1)) / 1024} GB"
        else:
            return "Unknown"
    elif platform.system() == 'Darwin':
        gpu_info = subprocess.check_output('/usr/sbin/system_profiler SPDisplaysDataType', shell=True).decode('utf-8')
        match = re.search(r'Chipset Model: (.*?)\n', gpu_info)
        if match:
            return match.group(1)
        else:
            return "Unknown"
    else:
        return "Unknown"

def get_installed_browsers():
    # Create a list to store information about installed browsers
    browsers = []
    if platform.system() == 'Darwin':
        # List of browser paths on macOS
        browser_paths = [
            "/Applications/Google Chrome.app",
            "/Applications/Firefox.app",
            "/Applications/Safari.app",
            # Add other browser paths as needed
        ]
        # Check for the presence of each browser by path and add it to the list
        for path in browser_paths:
            if os.path.exists(path):
                browsers.append(os.path.basename(path))
    return browsers

def save_system_info_to_file(system_info, filename):
    # Open the file to write system information
    with open(filename, 'w') as file:
        # Write each key-value pair to the file
        for key, value in system_info.items():
            file.write(f'{key}: {value}\n')

def main():
    # Get system information
    system_info = get_system_info()
    # Add information about installed browsers to the dictionary
    system_info['Installed Browsers'] = get_installed_browsers()
    # Save system information to a file
    save_system_info_to_file(system_info, 'system_info.txt')

if __name__ == '__main__':
    main()
