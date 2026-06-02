print("=== SOC Username Generator ===")
first_name = input("Enter first name: ")
last_name = input("Enter last name: ")
department = input("Enter department: SOC, IT, HR: ")

first = first_name.lower().strip()
last = last_name.lower().strip()
dept = department.lower().strip()

username1 = f"{first}.{last}"
username2 = f"{first[0]}{last}"
email = f"{first}.{last}@{dept}.company.com"

print("\n--- Generated Accounts ---")
print(f"Standard username: {username1}")
print(f"Short username: {username2}")
print(f"Email address: {email}")
