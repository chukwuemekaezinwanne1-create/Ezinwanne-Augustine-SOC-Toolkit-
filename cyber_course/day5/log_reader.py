print("=== SOC Log Analyzer ===")
print("Scanning for hacker activity...")

# Create fake attack log for practice
log_data = """INFO: User admin logged in from 192.168.1.10
ERROR: FAILED LOGIN for user root from 203.0.113.5
INFO: Backup completed successfully  
ERROR: FAILED LOGIN for user admin from 203.0.113.5
WARNING: Multiple failed attempts from 203.0.113.5
INFO: User augustine logged in from 192.168.1.20
ERROR: FAILED LOGIN for user test from 198.51.100.7"""

# Write log to file so we can read it like real SOC
with open("attack.log", "w") as f:
    f.write(log_data)

print("\n--- ALERTS FOUND ---")

# Read and analyze the log file
with open("attack.log", "r") as f:
    line_number = 0
    for line in f:
        line_number += 1
        if "FAILED LOGIN" in line:
            print(f"Line {line_number}: {line.strip()}")
        if "203.0.113.5" in line:
            print(f"THREAT IP DETECTED on Line {line_number}")

print("\nDay 5 complete. You just did threat hunting.")

