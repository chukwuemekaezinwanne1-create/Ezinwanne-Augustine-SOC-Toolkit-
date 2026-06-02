print("=== SOC Password Auditor ===")
password = input("Enter password to check: ")

has_length = len(password) >= 8
has_number = any(char.isdigit() for char in password)
has_upper = any(char.isupper() for char in password)
has_lower = any(char.islower() for char in password)

print("\n--- Audit Results ---")
print(f"At least 8 characters: {has_length}")
print(f"Contains number: {has_number}")
print(f"Contains uppercase: {has_upper}")
print(f"Contains lowercase: {has_lower}")

if has_length and has_number and has_upper and has_lower:
    print("\nStatus: STRONG ✅ Approved for SOC use")
else:
    print("\nStatus: WEAK ❌ Hackers will crack this in 2 mins")
    print("Fix: Use 8+ chars, upper, lower, and number")

print("Day 3 complete. Tool #2 added to portfolio.")
