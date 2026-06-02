import socket
import struct
import textwrap
from datetime import datetime

print("=== SOC Network Sniffer ===")
print("Day 13 - Traffic Analysis Tool - 100% Offline\n")

def get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr)
    return ':'.join(bytes_str).upper()

def get_ip(addr):
    return '.'.join(map(str, addr))

def ethernet_frame(data):
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto), data[14:]

def ipv4_packet(data):
    version_header_length = data[0]
    version = version_header_length >> 4
    header_length = (version_header_length & 15) * 4
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    return version, header_length, ttl, proto, get_ip(src), get_ip(target), data[header_length:]

def tcp_segment(data):
    src_port, dest_port, sequence, acknowledgment, offset_reserved_flags = struct.unpack('! H H L L H', data[:14])
    offset = (offset_reserved_flags >> 12) * 4
    flag_urg = (offset_reserved_flags & 32) >> 5
    flag_ack = (offset_reserved_flags & 16) >> 4
    flag_psh = (offset_reserved_flags & 8) >> 3
    flag_rst = (offset_reserved_flags & 4) >> 2
    flag_syn = (offset_reserved_flags & 2) >> 1
    flag_fin = offset_reserved_flags & 1
    return src_port, dest_port, sequence, acknowledgment, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data[offset:]

def udp_segment(data):
    src_port, dest_port, size = struct.unpack('! H H 2x H', data[:8])
    return src_port, dest_port, size, data[8:]

def format_multi_line(prefix, string, size=80):
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
        if size % 2:
            size -= 1
    return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])

def main():
    try:
        conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    except PermissionError:
        print("🚨 ERROR: Run with sudo or as root. Termux: use 'tsu' then run again.")
        print("If you can't get root, skip live capture and review the code logic.")
        return
    except Exception as e:
        print(f"🚨 ERROR: {e}")
        print("Note: Raw sockets need root. This is normal SOC behavior.")
        return
    
    print("Starting capture... Press CTRL+C to stop\n")
    packet_count = 0
    
    try:
        while packet_count < 5:
            raw_data, addr = conn.recvfrom(65536)
            dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
            print(f"\n=== PACKET #{packet_count + 1} ===")
            print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
            print(f"Ethernet: {src_mac} -> {dest_mac}")
            
            if eth_proto == 8:
                version, header_length, ttl, proto, src, target, data = ipv4_packet(data)
                print(f"IPv4: {src} -> {target} | TTL: {ttl} | Protocol: {proto}")
                
                if proto == 6:
                    src_port, dest_port, sequence, acknowledgment, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data = tcp_segment(data)
                    print(f"TCP: {src}:{src_port} -> {target}:{dest_port}")
                    flags = []
                    if flag_syn: flags.append("SYN")
                    if flag_ack: flags.append("ACK")
                    if flag_fin: flags.append("FIN")
                    if flag_rst: flags.append("RST")
                    if flag_psh: flags.append("PSH")
                    if flag_urg: flags.append("URG")
                    print(f"Flags: {' '.join(flags) if flags else 'None'}")
                    
                    # SOC Detection Logic
                    if flag_syn and not flag_ack:
                        print("🚨 ALERT: SYN scan detected - Possible port scan")
                        print("Action: LOG SOURCE IP + CHECK FIREWALL")
                    if dest_port == 4444 or dest_port == 1337:
                        print("🚨 CRITICAL: Suspicious port detected - Common malware C2")
                        print("Action: ISOLATE HOST + ESCALATE TO L2")
                    if dest_port == 443 or dest_port == 80:
                        print("✅ INFO: Web traffic detected")
                
                elif proto == 17:
                    src_port, dest_port, length, data = udp_segment(data)
                    print(f"UDP: {src}:{src_port} -> {target}:{dest_port} | Length: {length}")
                    if dest_port == 53:
                        print("✅ INFO: DNS query detected")
                    if dest_port == 1900:
                        print("⚠️ WARNING: SSDP traffic - Possible IoT scan")
                
                elif proto == 1:
                    print("ICMP: Ping/Echo detected")
                    print("⚠️ WARNING: ICMP can be used for tunneling")
                
            packet_count += 1
    
    except KeyboardInterrupt:
        print("\n\nCapture stopped by user")
    
    print(f"\nDay 13 complete. Captured {packet_count} packets. Tool #12 added to portfolio.")
    print("SOC Lesson: SYN without ACK = port scan. Port 4444 = Metasploit. Learn the patterns.")

if __name__ == "__main__":
    main()

