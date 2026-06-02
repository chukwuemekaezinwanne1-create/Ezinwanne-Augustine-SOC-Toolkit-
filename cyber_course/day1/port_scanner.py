import socket
print("=== Day 1: Port Scanner ===")
target = input("Target IP [127.0.0.1]: ") or "127.0.0.1"
ports = [22, 80, 443, 445, 3389]
print(f"Scanning {target}...")
for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((target, port))
    if result == 0:
        print(f"✅ Port {port}: OPEN")
    sock.close()
print("Day 1 complete.")
