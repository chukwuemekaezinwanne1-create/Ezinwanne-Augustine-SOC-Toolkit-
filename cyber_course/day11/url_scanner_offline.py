import re
from urllib.parse import urlparse

print("=== SOC URL Scanner - OFFLINE MODE ===")
print("Day 11 - Phishing URL Analysis Tool - No Data Required\n")

SUSPICIOUS_KEYWORDS = ['login', 'verify', 'account', 'secure', 'update', 'paypal', 'bank', 'signin']
SUSPICIOUS_TLDS = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club']

def analyze_url(url):
    if not url.startswith('http'):
        url = 'http://' + url
    
    parsed = urlparse(url)
    domain = parsed.netloc
    score = 0
    reasons = []
    
    print(f"Analyzing: {url}")
    print("--- THREAT ANALYSIS ---\n")
    
    # 1. Suspicious TLD
    if any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS):
        score += 3
        reasons.append(f"🚨 CRITICAL: Suspicious TLD detected: {domain}")
    else:
        reasons.append(f"✅ TLD appears normal: {domain}")
    
    # 2. Keyword check
    found_keywords = [k for k in SUSPICIOUS_KEYWORDS if k in url.lower()]
    if found_keywords:
        score += 2
        reasons.append(f"🚨 CRITICAL: Phishing keywords found: {', '.join(found_keywords)}")
    
    # 3. IP address instead of domain
    if re.match(r'^\d+\.\d+\.\d+\.\d+', domain):
        score += 3
        reasons.append(f"🚨 CRITICAL: Direct IP address used instead of domain")
    
    # 4. @ symbol trick - common in phishing
    if '@' in url:
        score += 2
        reasons.append(f"🚨 CRITICAL: @ symbol detected - possible credential theft")
    
    # 5. Too many subdomains
    if domain.count('.') > 3:
        score += 1
        reasons.append(f"⚠️ Warning: Excessive subdomains detected")
    
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
    
    print("\nDay 11 complete. Tool #10B added to portfolio.")

target_url = input("Enter URL to scan: ").strip()
analyze_url(target_url)

