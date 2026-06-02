import socket
print("=== Day 2: Banner Grabber ===")
target = input("Target IP [127.0.0.1]: ") or "127.0.0.1"
port = int(input("Port [80]: ") or 80)
try:
    s = socket.socket()
    s.settimeout(2)
    s.connect((target, port))
    s.send(b"HEAD / HTTP/1.0\r\n\r\n")
    banner = s.recv(1024).decode().strip()
    print(f"Banner:\n{banner[:200]}")
    s.close()
except: print("No banner or port closed")
print("Day 2 complete.")

