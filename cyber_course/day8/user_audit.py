import pwd, os
print("=== Day 8: User Audit ===")
users = pwd.getpwall()
suspicious = []
for user in users:
    if user.pw_uid == 0 and user.pw_name!= "root":
        suspicious.append(f"UID 0: {user.pw_name}")
    if user.pw_shell in ["/bin/bash", "/bin/sh"] and user.pw_uid >= 1000:
        print(f"✅ Normal user: {user.pw_name}")
if suspicious:
    print(f"🚨 ALERT: {suspicious}")
else:
    print("✅ No suspicious UID 0 accounts")
print("Day 8 complete.")

