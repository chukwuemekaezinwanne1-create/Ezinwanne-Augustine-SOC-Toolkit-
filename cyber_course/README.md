# Augustine's SOC Analyst Portfolio

**Goal:** Level 1 SOC Analyst at Flutterwave / Interswitch / Moniepoint 

**Tools Built:** 14 Python Security Scripts on Android Termux 

**GitHub:** github.com/chukwuemekaezinwanne1-create 

**Contact:** chukwuemekaezinwanne1@gmail.com 

**Location:** Nigeria | Available for remote/on-site

---

## Tools Overview

| Tool | SOC Use Case | Key Skills Demonstrated |
| --- | --- | --- |
| ip_validator.py | Input sanitization for firewalls | IP validation, error handling |
| password_checker.py | Enforce NIST password policy | Strings, conditionals, security standards |
| log_parser.py | Extract IOCs from raw logs | File I/O, regex thinking, data extraction |
| ip_validator_v2.py | Detect private vs public IPs | CIDR notation, network segmentation |
| log_analyzer.py | Detect brute force attacks | Log analysis, alerting, TTP detection |
| port_scanner.py | Find exposed services | Sockets, TCP, risk assessment |
| Coming soon | SIEM, Hashing, APIs | Incident response workflow |

## Day 1: IP Validator

**SOC Problem:** Firewalls fail when given malformed IPs like `256.1.1.1`. Analysts must sanitize input first. 

**Code:**
```python
print("*** SOC IP Validator ***")
ip = input("Enter IP to validate: ")
octets = ip.split('.')

if len(octets) != 4:
    print("Invalid IP - must have 4 octets")
else:
    valid = True
    for octet in octets:
        if not octet.isdigit() or not 0 <= int(octet) <= 255:
            valid = False
            break
    
    if valid:
        print(f"Valid IP: {ip}")
    else:
        print("Invalid IP - octet out of range 0-255")

