#!/data/data/com.termux/files/usr/bin/python
import os, subprocess
from datetime import datetime

NAME = "AUGUSTINE"
LOCATION = "Enugu"
STATUS = "GREEN"

def get_python_tools():
    return [
        "Port Scanner - Day 1/6/10",
        "Banner Grabber - Day 2",
        "Subdomain Finder - Day 3",
        "Hash Checker - Day 7",
        "User Audit - Day 8",
        "Log Analyzer - Day 9",
        "Vuln Scanner - Day 10",
        "URL Scanner - Day 11",
        "File Integrity - Day 12",
        "Packet Sniffer - Day 13",
        "IP Validator - Day 4",
        "SOC Dashboard - Day 14"
    ]

def get_cli_tools():
    try:
        result = subprocess.run(['pkg', 'list-installed'], capture_output=True, text=True, timeout=5)
        tools = []
        for line in result.stdout.split('\n'):
            if '/' in line and 'installed' in line:
                tool = line.split('/')[0].strip()
                if tool and tool not in ['base-files']: tools.append(tool)
        return sorted(set(tools))
    except:
        return ["nmap", "curl", "whois", "tcpdump"]

def generate_dashboard():
    py_tools = get_python_tools()
    cli_tools = get_cli_tools()
    total = len(py_tools) + len(cli_tools)

    os.system('clear')
    print(f"=== {NAME} SOC TOOLKIT | {LOCATION} | {total} TOOLS | {STATUS} ===")
    print("=")
    print("Threat Score: 95/100")
    print("-" * 55)

    counter = 1
    for tool in py_tools:
        print(f"{counter:3}. {tool}")
        counter += 1

    print("-" * 55)
    print(f"[+] CLI Tools Starting at #{counter}")
    print("-" * 55)

    # NO CAP - SHOW ALL CLI TOOLS
    for tool in cli_tools:
        print(f"{counter:3}. {tool}")
        counter += 1

    print("-" * 55)
    print(f"[+] Custom Python Tools: {len(py_tools)}")
    print(f"[+] CLI Arsenal: {len(cli_tools)}")
    print(f"[+] Total Arsenal: {total} TOOLS")
    print("=" * 55)

if __name__ == "__main__":
    generate_dashboard()
