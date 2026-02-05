#!/usr/bin/env python3
import sys
import re
import time
import argparse
import subprocess
import platform

# --- Banner & Colors ---
# ANSI escape codes for colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    banner = f"""
{Colors.BOLD}{Colors.CYAN}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  {Colors.GREEN}██████╗ ██╗██████╗ ███████╗████████╗███████╗██████╗ {Colors.CYAN}║
║  {Colors.GREEN}██╔══██╗██║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗{Colors.CYAN}║
║  {Colors.GREEN}██████╔╝██║██████╔╝█████╗     ██║   █████╗  ██████╔╝{Colors.CYAN}║
║  {Colors.GREEN}██╔══██╗██║██╔══██╗██╔══╝     ██║   ██╔══╝  ██╔══██╗{Colors.CYAN}║
║  {Colors.GREEN}██║  ██║██║██████╔╝███████╗   ██║   ███████╗██║  ██║{Colors.CYAN}║
║  {Colors.GREEN}╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝{Colors.CYAN}║
║                                                              ║
║  {Colors.BOLD}{Colors.WARNING}        >> Advanced MAC Address Recon Tool <<        {Colors.CYAN}║
║                                                              ║
║  {Colors.BOLD}Author: Azod814{Colors.ENDC}{Colors.CYAN}                                    ║
║  {Colors.BOLD}GitHub: github.com/azod814{Colors.ENDC}{Colors.CYAN}                        ║
╚══════════════════════════════════════════════════════════════╝
{Colors.ENDC}
"""
    print(banner)

# --- Helper Functions ---
def is_valid_mac(mac):
    """Validates MAC address format."""
    mac_regex = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$|^([0-9A-Fa-f]{4}\.[0-9A-Fa-f]{4}\.[0-9A-Fa-f]{4})$')
    return bool(mac_regex.match(mac))

def install_libraries():
    """Installs required libraries."""
    print(f"{Colors.WARNING}[!] This tool requires 'requests' and 'python-nmap'. Installing now...{Colors.ENDC}")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "python-nmap"])
        print(f"{Colors.GREEN}[+] Libraries installed successfully. Please run the script again.{Colors.ENDC}")
        sys.exit(0)
    except subprocess.CalledProcessError:
        print(f"{Colors.FAIL}[-] Failed to install libraries. Please run 'pip install requests python-nmap' manually.{Colors.ENDC}")
        sys.exit(1)

# --- Core Functions ---
def get_vendor_info(mac_address):
    """Fetches vendor information using macvendors.com API."""
    try:
        import requests
    except ImportError:
        install_libraries()

    try:
        url = f"https://api.macvendors.com/{mac_address}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 404:
            return "Vendor not found in database."
        else:
            return f"Error: HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Could not connect to API: {e}"

def scan_network_for_mac(target_mac, network_range="192.168.1.0/24"):
    """Scans the local network to find a device by its MAC address."""
    try:
        import nmap
    except ImportError:
        install_libraries()
        return # Exit after trying to install

    try:
        nm = nmap.PortScanner()
        print(f"\n{Colors.BLUE}[*] Scanning network: {network_range} for MAC {target_mac}...{Colors.ENDC}")
        print(f"{Colors.WARNING}[!] This may take a moment...{Colors.ENDC}")
        
        # Perform a fast ARP scan
        result = nm.scan(hosts=network_range, arguments='-sn')
        
        found = False
        for host in nm.all_hosts():
            if 'mac' in nm[host]['addresses']:
                found_mac = nm[host]['addresses']['mac'].upper()
                if found_mac == target_mac.upper():
                    ip = nm[host]['addresses']['ipv4']
                    hostname = nm[host].hostname() or "N/A"
                    print(f"\n{Colors.GREEN}[+] Device Found on Network!{Colors.ENDC}")
                    print(f"  {Colors.BOLD}IP Address:{Colors.ENDC} {ip}")
                    print(f"  {Colors.BOLD}Hostname:{Colors.ENDC} {hostname}")
                    print(f"  {Colors.BOLD}MAC Address:{Colors.ENDC} {found_mac}")
                    found = True
                    break
        
        if not found:
            print(f"\n{Colors.FAIL}[-] Device with MAC {target_mac} not found on the local network.{Colors.ENDC}")
            print(f"{Colors.WARNING}[!] Ensure you are on the same network and the device is online.{Colors.ENDC}")

    except nmap.nmap.PortScannerNotInstalledError:
        print(f"{Colors.FAIL}[-] 'nmap' is not installed on this system.{Colors.ENDC}")
        if platform.system() == "Linux":
            print(f"{Colors.WARNING}[!] On Debian/Ubuntu, install it with: sudo apt update && sudo apt install nmap -y{Colors.ENDC}")
        elif platform.system() == "Windows":
            print(f"{Colors.WARNING}[!] Please download and install Nmap from https://nmap.org/download.html{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}[-] An error occurred during scan: {e}{Colors.ENDC}")

# --- Main Menu ---
def main_menu():
    while True:
        print(f"\n{Colors.BOLD}{Colors.GREEN}--- Main Menu ---{Colors.ENDC}")
        print(f"{Colors.BOLD}1.{Colors.ENDC} {Colors.CYAN}Lookup Vendor Information{Colors.ENDC}")
        print(f"{Colors.BOLD}2.{Colors.ENDC} {Colors.CYAN}Scan Local Network for Device{Colors.ENDC}")
        print(f"{Colors.BOLD}3.{Colors.ENDC} {Colors.FAIL}Exit{Colors.ENDC}")
        
        choice = input(f"\n{Colors.BOLD}{Colors.WARNING}Enter your choice [1-3]: {Colors.ENDC}")

        if choice == '1':
            mac = input(f"{Colors.BOLD}Enter MAC Address (e.g., AA:BB:CC:DD:EE:FF): {Colors.ENDC}")
            if is_valid_mac(mac):
                print(f"\n{Colors.BLUE}[*] Looking up vendor for {mac}...{Colors.ENDC}")
                vendor = get_vendor_info(mac)
                print(f"{Colors.GREEN}[+] Vendor: {vendor}{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}[-] Invalid MAC address format. Please try again.{Colors.ENDC}")
        
        elif choice == '2':
            mac = input(f"{Colors.BOLD}Enter MAC Address to find on network: {Colors.ENDC}")
            if is_valid_mac(mac):
                # Auto-detect network range if possible (simplified)
                network_range = "192.168.1.0/24" # Default, can be made dynamic
                scan_network_for_mac(mac, network_range)
            else:
                print(f"{Colors.FAIL}[-] Invalid MAC address format. Please try again.{Colors.ENDC}")

        elif choice == '3':
            print(f"{Colors.WARNING}[*] Exiting...{Colors.ENDC}")
            sys.exit(0)
        
        else:
            print(f"{Colors.FAIL}[-] Invalid choice. Please enter a number between 1 and 3.{Colors.ENDC}")
        time.sleep(1.5) # Pause before showing menu again

if __name__ == "__main__":
    try:
        print_banner()
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] User interrupted. Exiting gracefully...{Colors.ENDC}")
        sys.exit(0)
