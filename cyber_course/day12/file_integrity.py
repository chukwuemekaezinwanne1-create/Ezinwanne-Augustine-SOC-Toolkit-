import os
import hashlib
import json
from datetime import datetime

print("=== SOC File Integrity Monitor ===")
print("Day 12 - HIDS Tripwire Tool - 100% Offline\n")

BASELINE_FILE = "baseline.json"

def get_file_hash(filepath):
    try:
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except:
        return None

def create_baseline(directory):
    print(f"Creating baseline for: {directory}")
    baseline = {}
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            file_hash = get_file_hash(filepath)
            if file_hash:
                mtime = os.path.getmtime(filepath)
                baseline[filepath] = {
                    "hash": file_hash,
                    "modified": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    "size": os.path.getsize(filepath)
                }
    
    with open(BASELINE_FILE, 'w') as f:
        json.dump(baseline, f, indent=2)
    
    print(f"✅ Baseline saved: {len(baseline)} files tracked in {BASELINE_FILE}")
    print("Action: Store this baseline file securely. This is your 'known good' state.")

def check_integrity(directory):
    if not os.path.exists(BASELINE_FILE):
        print(f"🚨 CRITICAL: No baseline found. Run with 'baseline' mode first.")
        return
    
    with open(BASELINE_FILE, 'r') as f:
        baseline = json.load(f)
    
    print(f"Checking integrity against baseline: {BASELINE_FILE}")
    print("--- INTEGRITY SCAN ---\n")
    
    current_files = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            current_files[filepath] = get_file_hash(filepath)
    
    modified = []
    new_files = []
    deleted = []
    
    # Check for modified and deleted files
    for filepath, data in baseline.items():
        if filepath not in current_files:
            deleted.append(filepath)
        elif current_files[filepath]!= data["hash"]:
            modified.append(filepath)
    
    # Check for new files
    for filepath in current_files:
        if filepath not in baseline:
            new_files.append(filepath)
    
    # Report results
    if not modified and not new_files and not deleted:
        print("✅ INTEGRITY INTACT: No changes detected")
        print("Verdict: LIKELY SAFE")
        print("Action: Continue monitoring")
    else:
        print(f"🚨 ALERT: {len(modified) + len(new_files) + len(deleted)} changes detected\n")
        
        if modified:
            print("CRITICAL: MODIFIED FILES:")
            for f in modified:
                print(f" - {f}")
        
        if new_files:
            print("\nWARNING: NEW FILES:")
            for f in new_files:
                print(f" - {f}")
        
        if deleted:
            print("\nWARNING: DELETED FILES:")
            for f in deleted:
                print(f" - {f}")
        
        print(f"\nThreat Score: {len(modified)*3 + len(new_files) + len(deleted)*2}/10")
        print("Verdict: POTENTIAL COMPROMISE")
        print("Action: ISOLATE SYSTEM + ESCALATE TO L2 + INVESTIGATE CHANGES")
    
    print("\nDay 12 complete. Tool #11 added to portfolio.")

# Main execution
mode = input("Mode [baseline/check]: ").strip().lower()
target_dir = input("Enter directory to monitor: ").strip()

if not os.path.exists(target_dir):
    print(f"Error: Directory {target_dir} does not exist")
else:
    if mode == "baseline":
        create_baseline(target_dir)
    elif mode == "check":
        check_integrity(target_dir)
    else:
        print("Invalid mode. Use 'baseline' or 'check'")
