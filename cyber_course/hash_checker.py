import hashlib

print("=== SOC Hash Checker ===")
print("Malware Detector - Day 7")

file_name = input("Enter filename to check: ")

try:
    with open(file_name, "rb") as f:
        file_data = f.read()
        md5_hash = hashlib.md5(file_data).hexdigest()
        sha256_hash = hashlib.sha256(file_data).hexdigest()
    
    print(f"\nFile: {file_name}")
    print(f"MD5:    {md5_hash}")
    print(f"SHA256: {sha256_hash}")
    
    # Check against known malware hash - EICAR test file
    eicar_md5 = "44d88612fea8a8f36de82e1278abb02f"
    
    print("\n--- THREAT ANALYSIS ---")
    if md5_hash == eicar_md5:
        print("CRITICAL ALERT: EICAR TEST VIRUS DETECTED!")
        print("Action: QUARANTINE FILE IMMEDIATELY")
    else:
        print("SAFE: Hash not in malware database")
        print("Action: Allow file")
        
except FileNotFoundError:
    print("ERROR: File not found. Check the name and try again.")

print("\nDay 7 complete. Tool #6 added to portfolio.")
