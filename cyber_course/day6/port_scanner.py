import socket

print("=== SOC Port Scanner ===")
target = input("Enter IP or website to scan: ")
print(f"Scanning {target} for open ports...")

# Common hacker target ports
ports = [21, 22, 23, 25, 53, 80, 443, 8080]
port_names = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 
    53: "DNS", 80: "HTTP", 443: "HTTPS", 8080: "HTTP-Alt"
}

open_ports = []

for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1) # 1 second timeout so it runs fast
    result = sock.connect_ex((target, port))
    
    if result == 0:
        print(f"Port {port} ({port_names[port]}) is OPEN - DANGER")
        open_ports.append(port)
    else:
        print(f"Port {port} ({port_names[port]}) is closed")
    sock.close()

print("\n--- SCAN COMPLETE ---")
if open_ports:
    print(f"ALERT: Found {len(open_ports)} open ports. Attackers can target these.")
    if 22 in open_ports:
        print("CRITICAL: SSH port 22 is open. Brute force risk!")
    if 23 in open_ports:
        print("CRITICAL: Telnet port 23 is open. Unencrypted!")
else:
    print("SAFE: No common ports open.")

print("Day 6 complete. Tool #5 added to portfolio.")

