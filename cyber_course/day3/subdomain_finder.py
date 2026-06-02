import socket
print("=== Day 3: Subdomain Finder - Offline ===")
domain = input("Domain [example.com]: ") or "example.com"
subs = ["www", "mail", "ftp", "test", "dev"]
print(f"Checking {domain}...")
for sub in subs:
    try:
        full = f"{sub}.{domain}"
        socket.gethostbyname(full)
        print(f"✅ Found: {full}")
    except: pass
print("Day 3 complete.")
