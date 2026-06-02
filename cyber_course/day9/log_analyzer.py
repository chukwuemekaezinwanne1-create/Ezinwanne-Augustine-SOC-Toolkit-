import re
from collections import defaultdict

def analyze_auth_log(filename):
    failed_attempts = defaultdict(int)
    successful_logins = []
    total_fails = 0
    
    print("=== SOC Log Analyzer ===")
    print("Day 9 - Brute Force Detection Tool\n")
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                # Check for failed password
                fail_match = re.search(r'Failed password for.* from (\d+\.\d+\.\d+\.\d+)', line)
                if fail_match:
                    ip = fail_match.group(1)
                    failed_attempts[ip] += 1
                    total_fails += 1
                
                # Check for successful login
                success_match = re.search(r'Accepted password for (\w+) from (\d+\.\d+\.\d+\.\d+)', line)
                if success_match:
                    user = success_match.group(1)
                    ip = success_match.group(2)
                    successful_logins.append(f"{user} from {ip}")
    
    except FileNotFoundError:
        print(f"ERROR: {filename} not found")
        return
    
    # --- THREAT ANALYSIS ---
    print("--- THREAT ANALYSIS ---")
    print(f"Total failed login attempts: {total_fails}\n")
    
    # Flag IPs with 3+ failures
    alert_triggered = False
    print("Suspicious IPs - Possible Brute Force:")
    for ip, count in failed_attempts.items():
        if count >= 3:
            print(f"🚨 CRITICAL ALERT: {ip} → {count} failed attempts")
            print(f" Action: BLOCK IP IMMEDIATELY")
            alert_triggered = True
        else:
            print(f"⚠️ Warning: {ip} → {count} failed attempts")
    
    if not alert_triggered:
        print("✅ No brute force patterns detected")
    
    # Show successful logins
    print(f"\nSuccessful logins: {len(successful_logins)}")
    for login in successful_logins:
        print(f"✅ {login}")
    
    print("\nDay 9 complete. Tool #8 added to portfolio.")

filename = input("Enter log file to analyze: ")
analyze_auth_log(filename)

