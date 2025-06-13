# OSINT Investigator Hub

The OSINT Investigator Hub is a web-based Open-Source Intelligence (OSINT) tool developed using Flask, integrated with Kali Linux tools, designed exclusively for professional testing and ethical hacking purposes. This project aims to provide a secure and controlled environment for security researchers and professionals to conduct authorized assessments.

## Features
- Automated service management via systemd
- Web interface supporting tools such as Nmap, Shodan, and TheHarvester
- Customizable templates and static assets
- Virtual environment setup for dependency management

![Main Page Screenshot](imagens/screenshot-main-page.jpg)

## Purpose and Usage
This toolset is intended solely for professional testing and ethical hacking activities. It must be used in compliance with all applicable laws and regulations, with explicit permission from system owners or administrators. Unauthorized use or exploitation is strictly prohibited and may result in legal consequences.

## Developed By
Created by Banze007 to demonstrate expertise in web development, cybersecurity, and automation.

## Setup
1. Clone this repository: `git clone https://github.com/Banze007/osint-investigator-hub.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Start the service: `sudo systemctl start osint_tool.service`
4. Access the application at `http://127.0.0.1:5000`

## License
This project is released under the MIT License.
