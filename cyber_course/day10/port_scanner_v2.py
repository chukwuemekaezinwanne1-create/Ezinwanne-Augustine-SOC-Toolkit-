import socket
import threading
from queue import Queue

print("=== SOC Port Scanner V2 ===")
print("Day 10 - Service Detection + Banner Grabbing Tool\n")

# Common ports + services for banner grabbing
COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 
    53: "DNS", 80: "HTTP", 110: "POP3", 139: "NetBIOS",
    143: "IMAP", 443: "HTTPS", 445: "SMB", 3306: "MySQL",
    3389: "RDP", 8080: "HTTP-Alt"
}

open_ports = []
q = Queue()
print_lock = threading.Lock()

def grab_banner(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip, port))
        
        # Send HTTP request for web ports to get server header
        if port in [80, 443, 8080, 8443]:
            sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        sock.close()
        return banner.split('\n')[0] if banner else "No banner"
    except:
        return "No banner"

def scan_port(ip):
    while not q.empty():
        port = q.get()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            
            if result == 0:
                service = COMMON_PORTS.get(port, "Unknown")
                banner = grab_banner(ip, port)
                
                with print_lock:
                    print(f"[+] Port {port}/tcp OPEN | {service} | {banner[:50]}")
                    open_ports.append((port, service, banner))
            sock.close()
        except:
            pass
        q.task_done()

def run_scanner(target_ip, start_port, end_port, threads=100):
    print(f"Scanning {target_ip} ports {start_port}-{end_port}")
    print("--- THREAT ANALYSIS ---\n")
    
    # Fill queue
    for port in range(start_port, end_port + 1):
        q.put(port)
    
    # Start threads
    for _ in range(threads):
        t = threading.Thread(target=scan_port, args=(target_ip,))
        t.daemon = True
        t.start()
    
    q.join()
    
    # Final report
    print(f"\nScan complete. {len(open_ports)} open ports found.")
    if open_ports:
        print("\n🚨 SOC ACTION REQUIRED:")
        for port, service, banner in open_ports:
            if "Apache/2.4.49" in banner or "OpenSSH_7.4" in banner:
                print(f"CRITICAL: Port {port} {service} → Vulnerable version: {banner}")
                print(f"Action: ESCALATE TO L2 - Patch immediately")
    
    print("\nDay 10 complete. Tool #9 added to portfolio.")

target = input("Enter target IP: ")
start = int(input("Start port: "))
end = int(input("End port: "))
run_scanner(target, start, end)

