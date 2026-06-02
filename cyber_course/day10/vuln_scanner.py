import socket
print("=== Day 10: Vuln Scanner - Offline ===")
target = input("Target IP [127.0.0.1]: ") or "127.0.0.1"
risky_ports = {21:"FTP", 23:"Telnet", 445:"SMB", 3389:"RDP"}
print(f"Scanning {target} for risky services...")
vulns = 0
for port, service in risky_ports.items():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    if sock.connect_ex((target, port)) == 0:
        print(f"🚨 VULN: {service} on port {port} - Disable if unused")
        vulns += 1
    sock.close()
if vulns == 0: print("✅ No common risky ports open")
print(f"Threat Score: {vulns}/4")
print("Day 10 complete.")

