print("=== SOC IP Validator ===")
ip = input("Enter IP address to check: ")

parts = ip.split(".")

if len(parts) == 4:
    valid = True
    for part in parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            valid = False
    
    if valid:
        print(f"{ip} is VALID IP. Safe to investigate.")
    else:
        print(f"{ip} is INVALID. Hacker using fake IP.")
else:
    print(f"{ip} is INVALID. Needs exactly 4 parts.")

print("Day 4 complete. Tool #3 added to portfolio.")

