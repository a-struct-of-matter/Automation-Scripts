import socket
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

try:
    from ai_analyzer import GeminiAnalyzer, AIInsightCache
    from config import get_config
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

class PortScanner:
    """Scans ports and identifies open services."""
    
    # Common ports and their services
    COMMON_PORTS = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        5900: "VNC",
        8080: "HTTP-Alt",
        8443: "HTTPS-Alt",
    }
    
    # Vulnerability database
    VULNERABILITIES = {
        "FTP": [
            "Default credentials often used (ftp:ftp)",
            "Weak authentication mechanisms",
            "Unencrypted data transmission",
            "Outdated FTP servers prone to exploits"
        ],
        "SSH": [
            "Weak SSH key generation (if using old OpenSSH versions)",
            "SSH key exhaustion attacks possible",
            "Brute force attacks if weak credentials used",
            "CVE-2018-10933 (libssh) if older version"
        ],
        "Telnet": [
            "Unencrypted remote access",
            "Credentials transmitted in plaintext",
            "Serious security risk - should use SSH instead",
            "Susceptible to man-in-the-middle attacks"
        ],
        "SMTP": [
            "Open relay vulnerabilities",
            "Spam relay risks",
            "Enumeration of valid accounts possible",
            "Potential for email spoofing"
        ],
        "DNS": [
            "DNS amplification attacks possible",
            "DNS cache poisoning risks",
            "Zone transfer vulnerabilities",
            "DNS spoofing attacks possible"
        ],
        "HTTP": [
            "Data transmitted in plaintext",
            "Vulnerable to man-in-the-middle attacks",
            "Should upgrade to HTTPS",
            "Potential web application vulnerabilities"
        ],
        "HTTPS": [
            "SSL/TLS misconfiguration possible",
            "Certificate validation issues",
            "Weak cipher suites may be used",
            "Downgrade attacks if not properly configured"
        ],
        "POP3": [
            "Unencrypted email retrieval",
            "Credentials transmitted in plaintext",
            "Weak authentication mechanisms",
            "Should use POP3S (encrypted) instead"
        ],
        "IMAP": [
            "Unencrypted email access",
            "Plaintext credential transmission",
            "Weak authentication on some servers",
            "Should use IMAPS (encrypted) instead"
        ],
        "SMB": [
            "Windows file sharing vulnerabilities",
            "Ransomware propagation vector",
            "Eternal Blue exploit (CVE-2017-0144) if unpatched",
            "Null session enumeration possible",
            "Weak password policies exploitation"
        ],
        "MySQL": [
            "Default credentials (root:password) often present",
            "Unauthenticated access possible",
            "SQL injection vulnerabilities",
            "Remote root access if misconfigured"
        ],
        "RDP": [
            "Brute force attacks common",
            "BlueKeep vulnerability (CVE-2019-0708) if unpatched",
            "Weak passwords easily cracked",
            "Remote code execution possible"
        ],
        "PostgreSQL": [
            "Default credentials (postgres:password) sometimes used",
            "SQL injection attacks possible",
            "Weak password policies",
            "Unauthorized database access risks"
        ],
        "VNC": [
            "Weak default passwords",
            "Unencrypted screen sharing data",
            "Man-in-the-middle attack vectors",
            "Brute force vulnerable"
        ]
    }
    
    def __init__(self, timeout=2, use_ai=False, api_key=None):
        self.timeout = timeout
        self.open_ports = {}
        self.ai_analyzer = None
        self.ai_cache = AIInsightCache() if AI_AVAILABLE else None
        
        # Initialize AI if requested
        if use_ai and AI_AVAILABLE:
            try:
                self.ai_analyzer = GeminiAnalyzer(api_key=api_key)
                print("[+] AI Analyzer initialized successfully!")
            except Exception as e:
                print(f"[!] Could not initialize AI: {e}")
                print("[*] Continuing with standard analysis...")
    
    def scan_port(self, host, port):
        """Scan a single port on the target host."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = self.COMMON_PORTS.get(port, "Unknown")
                return port, service
            return None
        except socket.gaierror:
            print(f"\n[!] Hostname {host} could not be resolved.")
            sys.exit()
        except socket.error:
            print(f"\n[!] Could not connect to {host}.")
            sys.exit()
    
    def scan_range(self, host, start_port, end_port, threads=50):
        """Scan a range of ports using multi-threading."""
        print(f"\n[*] Scanning host {host}")
        print(f"[*] Scanning ports {start_port} to {end_port}")
        print(f"[*] Scan started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        open_ports = {}
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {
                executor.submit(self.scan_port, host, port): port 
                for port in range(start_port, end_port + 1)
            }
            
            completed = 0
            for future in as_completed(futures):
                completed += 1
                result = future.result()
                if result:
                    port, service = result
                    open_ports[port] = service
                    print(f"[+] Port {port}: {service} is OPEN")
                
                # Progress indicator
                if completed % 10 == 0:
                    progress = (completed / (end_port - start_port + 1)) * 100
                    print(f"    Progress: {progress:.1f}%")
        
        self.open_ports = open_ports
        return open_ports
    
    def scan_common_ports(self, host):
        """Scan only common ports."""
        print(f"\n[*] Scanning common ports on {host}")
        print(f"[*] Scan started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        open_ports = {}
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {
                executor.submit(self.scan_port, host, port): port 
                for port in self.COMMON_PORTS.keys()
            }
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    port, service = result
                    open_ports[port] = service
                    print(f"[+] Port {port}: {service} is OPEN")
        
        self.open_ports = open_ports
        return open_ports
    
    def get_vulnerabilities(self, service):
        """Get potential vulnerabilities for a service."""
        return self.VULNERABILITIES.get(service, [
            "Service identified but specific vulnerabilities not in database",
            "Recommend manual review of service documentation"
        ])
    
    def generate_report(self, host, use_ai=False):
        """Generate a detailed vulnerability report with optional AI insights."""
        print("\n" + "="*70)
        print("VULNERABILITY ASSESSMENT REPORT")
        print("="*70)
        print(f"Target Host: {host}")
        print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Open Ports Found: {len(self.open_ports)}\n")
        
        if not self.open_ports:
            print("[*] No open ports found.")
            return
        
        for port in sorted(self.open_ports.keys()):
            service = self.open_ports[port]
            print(f"\n[PORT {port}] {service}")
            print("-" * 70)
            vulnerabilities = self.get_vulnerabilities(service)
            for idx, vuln in enumerate(vulnerabilities, 1):
                print(f"  {idx}. {vuln}")
            
            # Get AI analysis if enabled
            if use_ai and self.ai_analyzer:
                print(f"\n[AI ANALYSIS] {service}")
                print("-" * 70)
                analysis = self.ai_analyzer.analyze_port(port, service, vulnerabilities)
                print(analysis)
        
        print("\n" + "="*70)
        print("RECOMMENDATIONS:")
        print("="*70)
        print("1. Update all services to the latest patched versions")
        print("2. Implement firewalls and access controls")
        print("3. Use encryption (HTTPS, SSH, etc.) for data transmission")
        print("4. Implement strong authentication mechanisms")
        print("5. Regular security audits and penetration testing")
        print("6. Monitor logs for suspicious activities")
        print("7. Disable unnecessary services")
        
        # AI-powered recommendations
        if use_ai and self.ai_analyzer:
            print("\n[AI-POWERED INSIGHTS]")
            print("-" * 70)
            report = self.ai_analyzer.generate_security_report(host, self.open_ports)
            print(report)
        
        print("="*70 + "\n")
    
    def export_json(self, host, filename):
        """Export scan results to JSON."""
        report = {
            "host": host,
            "scan_time": datetime.now().isoformat(),
            "open_ports": self.open_ports,
            "vulnerabilities": {
                port: {
                    "service": self.open_ports[port],
                    "risks": self.get_vulnerabilities(self.open_ports[port])
                }
                for port in self.open_ports
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"[+] Report exported to {filename}")
    
    def get_remediation(self, service: str, vulnerability: str) -> str:
        """Get AI-powered remediation steps for a vulnerability."""
        if not self.ai_analyzer:
            return "AI analyzer not available. Get an API key to enable this feature."
        return self.ai_analyzer.get_remediation(service, vulnerability)
    
    def ask_ai_question(self, question: str) -> str:
        """Ask the AI analyzer a security question."""
        if not self.ai_analyzer:
            return "AI analyzer not available. Get an API key to enable this feature."
        return self.ai_analyzer.ask_security_question(question)
    
    def get_cve_info(self, service: str) -> str:
        """Get CVE information for a service."""
        if not self.ai_analyzer:
            return "AI analyzer not available. Get an API key to enable this feature."
        return self.ai_analyzer.get_cve_info(service)
    
    def get_hardening_guide(self, service: str) -> str:
        """Get comprehensive hardening guide for a service."""
        if not self.ai_analyzer:
            return "AI analyzer not available. Get an API key to enable this feature."
        return self.ai_analyzer.get_hardening_guide(service)


def get_user_input():
    """Get interactive input from user."""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   Port Scanner & Vulnerability Assessment Tool v1.0      ║
    ║            Educational Security Learning Tool            ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    print("\n[*] LEGAL NOTICE: Only scan systems you own or have explicit permission to test.\n")
    
    # Get target host
    while True:
        host = input("Enter target host (IP or hostname): ").strip()
        if host:
            break
        print("[!] Please enter a valid host.")
    
    # Get scan type
    print("\n[*] Scan Options:")
    print("    1. Scan common ports (recommended for learning)")
    print("    2. Scan custom port range")
    
    while True:
        scan_type = input("\nSelect scan type (1 or 2): ").strip()
        if scan_type in ['1', '2']:
            break
        print("[!] Please enter 1 or 2.")
    
    scan_common = scan_type == '1'
    start_port = 1
    end_port = 1024
    
    if not scan_common:
        # Get port range
        while True:
            try:
                start_port = int(input("Enter start port (default 1): ").strip() or "1")
                if 1 <= start_port <= 65535:
                    break
                print("[!] Port must be between 1 and 65535.")
            except ValueError:
                print("[!] Please enter a valid port number.")
        
        while True:
            try:
                end_port = int(input(f"Enter end port (default 1024): ").strip() or "1024")
                if 1 <= end_port <= 65535 and end_port >= start_port:
                    break
                print(f"[!] End port must be between {start_port} and 65535.")
            except ValueError:
                print("[!] Please enter a valid port number.")
    
    # Get number of threads
    while True:
        try:
            threads = int(input("Enter number of threads (default 50): ").strip() or "50")
            if 1 <= threads <= 500:
                break
            print("[!] Threads should be between 1 and 500.")
        except ValueError:
            print("[!] Please enter a valid number.")
    
    # Ask to export to JSON
    export_json = False
    json_file = None
    while True:
        export = input("\nExport results to JSON? (y/n, default n): ").strip().lower()
        if export in ['y', 'n', '']:
            export_json = export == 'y'
            break
        print("[!] Please enter 'y' or 'n'.")
    
    if export_json:
        while True:
            json_file = input("Enter JSON filename (default: report.json): ").strip() or "report.json"
            if json_file:
                break
            print("[!] Please enter a valid filename.")
    
    # Ask to enable AI features
    use_ai = False
    api_key = None
    if AI_AVAILABLE:
        print("\n[*] AI Features Available (requires Gemini API key)")
        while True:
            ai_choice = input("Use AI-powered analysis? (y/n, default n): ").strip().lower()
            if ai_choice in ['y', 'n', '']:
                use_ai = ai_choice == 'y'
                break
            print("[!] Please enter 'y' or 'n'.")
        
        if use_ai:
            config_obj = get_config()
            api_key = config_obj.get_api_key()
            
            if not api_key:
                print("\n[!] No API key found.")
                setup = input("Setup API key now? (y/n): ").strip().lower()
                if setup == 'y':
                    if config_obj.setup_api_key():
                        api_key = config_obj.get_api_key()
                    else:
                        use_ai = False
                        print("[*] Continuing without AI features...")
                else:
                    use_ai = False
    else:
        print("\n[*] AI features not available (google-generativeai not installed)")
        print("    Install with: pip install -r requirements.txt")
    
    return {
        'host': host,
        'scan_common': scan_common,
        'start_port': start_port,
        'end_port': end_port,
        'threads': threads,
        'export_json': export_json,
        'json_file': json_file,
        'use_ai': use_ai,
        'api_key': api_key
    }


def main():
    """Main function with interactive input."""
    config = get_user_input()
    
    # Initialize scanner with AI if enabled
    scanner = PortScanner(
        use_ai=config['use_ai'],
        api_key=config['api_key']
    )
    
    try:
        print("\n" + "="*70)
        if config['scan_common']:
            scanner.scan_common_ports(config['host'])
        else:
            scanner.scan_range(config['host'], config['start_port'], 
                             config['end_port'], config['threads'])
        
        # Generate report with AI if enabled
        scanner.generate_report(config['host'], use_ai=config['use_ai'])
        
        # Interactive AI features menu
        if config['use_ai'] and scanner.ai_analyzer:
            show_ai_menu(scanner, config['host'])
        
        if config['export_json']:
            scanner.export_json(config['host'], config['json_file'])
        
        print("\n[+] Scan completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error occurred: {str(e)}")
        sys.exit(1)


def show_ai_menu(scanner, host):
    """Show interactive AI features menu."""
    while True:
        print("\n" + "="*70)
        print("AI FEATURES MENU")
        print("="*70)
        print("1. Get hardening guide for a service")
        print("2. Get CVE information for a service")
        print("3. Ask a security question")
        print("4. Get remediation steps for a vulnerability")
        print("5. Back to main menu")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            service = input("Enter service name (e.g., SSH, MySQL): ").strip()
            if service:
                print("\n[*] Generating hardening guide...")
                guide = scanner.get_hardening_guide(service)
                print(guide)
        
        elif choice == '2':
            service = input("Enter service name (e.g., SSH, MySQL): ").strip()
            if service:
                print("\n[*] Fetching CVE information...")
                info = scanner.get_cve_info(service)
                print(info)
        
        elif choice == '3':
            question = input("Ask your security question: ").strip()
            if question:
                print("\n[*] Analyzing question...")
                answer = scanner.ask_ai_question(question)
                print(answer)
        
        elif choice == '4':
            service = input("Enter service name: ").strip()
            vuln = input("Enter vulnerability description: ").strip()
            if service and vuln:
                print("\n[*] Getting remediation steps...")
                remediation = scanner.get_remediation(service, vuln)
                print(remediation)
        
        elif choice == '5':
            break
        else:
            print("[!] Invalid option. Please try again.")


if __name__ == '__main__':
    main()
