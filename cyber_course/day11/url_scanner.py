import whois
import requests
import re
from urllib.parse import urlparse
from datetime import datetime

print("=== SOC URL Scanner ===")
print("Day 11 - Phishing URL Analysis Tool\n")

SUSPICIOUS_KEYWORDS = ['login', 'verify', 'account', 'secure', 'update', 'paypal', 'bank', 'signin']
SUSPICIOUS_TLDS = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz']

def check_domain_age(domain):
    try:
        w = whois.whois(domain)
        creation = w.creation_date
        if isinstance(creation, list):
            creation = creation[0]
        if creation:
            age_days = (datetime.now() - creation).days
            return age_days, creation.strftime("%Y-%m-%d")
        return None, "Unknown"
    except:
        return None, "WHOIS lookup failed"

def check_redirects(url):
    try:
        r = requests.head(url, timeout=5, allow_redirects=True)
        if len(r.history) > 0:
            return len(r.history), r.url
        return 0, url
    except:
        return -1, "Connection failed"

def analyze_url(url):
    if not url.startswith('http'):
        url = 'http://' + url
    
    parsed = urlparse(url)
    domain = parsed.netloc
    score = 0
    reasons = []
    
    print(f"Analyzing: {url}")
    print("--- THREAT ANALYSIS ---\n")
    
    # 1. Domain age check
    age, created = check_domain_age(domain)
    if age is not None:
        if age < 30:
            score += 3
            reasons.append(f"🚨 CRITICAL: Domain only {age} days old, created {created}")
        elif age < 90:
            score += 1
            reasons.append(f"⚠️ Warning: Domain {age} days old, created {created}")
        else:
            reasons.append(f"✅ Domain age: {age} days, created {created}")
    else:
        score += 2
        reasons.append(f"⚠️ Warning: {created}")
    
    # 2. Suspicious TLD
    if any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS):
        score += 2
        reasons.append(f"🚨 CRITICAL: Suspicious TLD detected in {domain}")
    
    # 3. Keyword check
    found_keywords = [k for k in SUSPICIOUS_KEYWORDS if k in url.lower()]
    if found_keywords:
        score += 1
        reasons.append(f"⚠️ Warning: Phishing keywords found: {', '.join(found_keywords)}")
    
    # 4. IP address instead of domain
    if re.match(r'^\d+\.\d+\.\d+\.\d+', domain):
        score += 3
        reasons.append(f"🚨 CRITICAL: Direct IP address used instead of domain")
    
    # 5. Redirect check
    redirect_count, final_url = check_redirects(url)
    if redirect_count > 2:
        score += 2
        reasons.append(f"🚨 CRITICAL: {redirect_count} redirects to {final_url}")
    elif redirect_count > 0:
        score += 1
        reasons.append(f"⚠️ Warning: {redirect_count} redirect to {final_url}")
    elif redirect_count == -1:
        score += 1
        reasons.append(f"⚠️ Warning: Could not connect to URL")
    
    # Final verdict
    for reason in reasons:
        print(reason)
    
    print(f"\nThreat Score: {score}/10")
    if score >= 5:
        print("Verdict: MALICIOUS - Phishing Likely")
        print("Action: BLOCK URL + ESCALATE TO L2")
    elif score >= 3:
        print("Verdict: SUSPICIOUS - Investigate further")
        print("Action: QUARANTINE EMAIL + WARN USER")
    else:
        print("Verdict: LIKELY SAFE")
        print("Action: Allow, but monitor")
    
    print("\nDay 11 complete. Tool #10 added to portfolio.")

target_url = input("Enter URL to scan: ")
analyze_url(target_url)

