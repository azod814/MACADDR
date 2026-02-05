# MAC-Recon

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.6%2B-green.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)]()

MAC-Recon is an advanced command-line utility designed for in-depth MAC address reconnaissance. It enables users to extract critical device information, ranging from manufacturer details to live network data such as IP address and hostname, all through a sleek and intuitive interface.

## ✨ Features

-   🎨 **Beautiful CLI Interface:** A visually appealing command-line experience with colors and an ASCII banner.
-   🏢 **Vendor Lookup:** Instantly identify the manufacturer of any device using its MAC address.
-   🔍 **Network Scanner:** Scan your local network to locate a specific device and retrieve its IP and hostname.
-   🌐 **Cross-Platform:** Fully compatible with Linux, Windows, and macOS.
-   ⚙️ **Auto-Installer:** Automatically installs required Python libraries for a seamless setup.

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/azod814/mac-recon.git
cd mac-recon



2. Make the Tool Executable (Linux/macOS)
bash

chmod +x mac_recon.py

3. Install Dependencies

The tool can attempt to install its dependencies, but it's recommended to do it manually for a smooth setup.
bash

pip3 install -r requirements.txt

⚠️ Important: The network scanning feature requires nmap to be installed on your system.

    On Debian/Ubuntu:
    bash

    sudo apt update && sudo apt install nmap -y

    On Fedora/CentOS:
    bash

    sudo dnf install nmap -y

    On Windows: Download and install from the official Nmap site.

🚀 Usage

Execute the tool using python3:
bash

python3 mac_recon.py
