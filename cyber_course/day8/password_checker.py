import re

def check_password_strength(password):
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 12:
        score += 2
        feedback.append("✅ Length: 12+ chars")
    elif len(password) >= 8:
        score += 1
        feedback.append("⚠️  Length: 8+ chars, but 12+ is better")
    else:
        feedback.append("❌ Length: Too short, use 8+ chars")
    
    # Uppercase check
    if re.search(r'[A-Z]', password):
        score += 1
        feedback.append("✅ Uppercase letter found")
    else:
        feedback.append("❌ Missing uppercase letter")
    
    # Lowercase check
    if re.search(r'[a-z]', password):
        score += 1
        feedback.append("✅ Lowercase letter found")
    else:
        feedback.append("❌ Missing lowercase letter")
    
    # Digit check
    if re.search(r'[0-9]', password):
        score += 1
        feedback.append("✅ Number found")
    else:
        feedback.append("❌ Missing number")
    
    # Special char check
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
        feedback.append("✅ Special character found")
    else:
        feedback.append("❌ Missing special character")
    
    # Common password check
    common = ['password', '123456', 'qwerty', 'admin', 'summer2025']
    if password.lower() in common:
        score = 0
        feedback.append("❌ CRITICAL: This is a top leaked password")
    
    # Final rating
    print("\n--- PASSWORD ANALYSIS ---")
    for f in feedback:
        print(f)
    
    print(f"\nScore: {score}/6")
    if score >= 5:
        print("Strength: STRONG - SOC approved")
        print("Action: Allow")
    elif score >= 3:
        print("Strength: MODERATE - Advise user to improve")
        print("Action: Warn")
    else:
        print("Strength: WEAK - Block in production")
        print("Action: REJECT")

print("=== SOC Password Checker ===")
print("Day 8 - User Account Hardening Tool")
pwd = input("Enter password to check: ")
check_password_strength(pwd)
print("\nDay 8 complete. Tool #7 added to portfolio.")

