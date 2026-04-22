os --> This package is used to retrive the meta data of the operating system like configurations, cpu usage, memory usage etc 
most important methods in this package are
-

====================================================================================================
IMPORTANT CYBERSECURITY PACKAGES FOR HACKERS/PENETRATION TESTERS
====================================================================================================

1. requests --> HTTP library for making web requests
   Useful Methods:
   - requests.get(url) --> Retrieve web pages
   - requests.post(url, data=payload) --> Send POST requests with payloads
   - requests.headers --> Send custom headers for bypassing restrictions
   - requests.cookies --> Handle session cookies
   - requests.auth --> Handle authentication
   Use case: Web scraping, API interaction, HTTP fuzzing

2. socket --> Low-level networking interface
   Useful Methods:
   - socket.socket() --> Create raw sockets for network communication
   - socket.connect((host, port)) --> Connect to remote servers
   - socket.bind() --> Bind to a port for listening
   - socket.recv(buffer_size) --> Receive data from connections
   - socket.send(data) --> Send raw data
   Use case: Port scanning, banner grabbing, custom protocols

3. subprocess --> Execute system commands from Python
   Useful Methods:
   - subprocess.run(command) --> Execute shell commands
   - subprocess.Popen() --> Create processes with piping capabilities
   - subprocess.check_output() --> Get command output
   Use case: Automating system exploits, executing multi-stage payloads

4. paramiko --> SSH/SFTP client library
   Useful Methods:
   - SSHClient.connect() --> Connect to SSH servers
   - SSHClient.exec_command() --> Execute remote commands
   - SFTPClient.get/put() --> Upload/download files
   Use case: Remote access, automated SSH exploitation, file exfiltration

5. scapy --> Powerful packet manipulation library
   Useful Methods:
   - IP()/TCP()/UDP() --> Create network packets
   - send(packet) --> Send crafted packets
   - sniff(iface, prn, filter) --> Capture and analyze network traffic
   - sr(packets) --> Send and receive packets
   Use case: Network scanning, packet crafting, ARP spoofing, DoS attacks

6. nmap --> Network scanning and mapping
   Useful Methods:
   - PortScannerAsync() --> Async port scanning
   - scan(hosts, ports) --> Scan target for open ports
   Use case: Service enumeration, vulnerability detection

7. beautifulsoup4 --> HTML/XML parsing
   Useful Methods:
   - BeautifulSoup(html_content) --> Parse HTML
   - soup.find_all(tag) --> Extract specific elements
   - soup.select(css_selector) --> CSS selector queries
   Use case: Web scraping, extracting sensitive data, finding injection points

8. sqlalchemy/sql-inject --> SQL manipulation and injection testing
   Useful Methods:
   - Execute raw SQL queries
   - Automate SQL injection payloads
   Use case: Database exploitation, SQL injection testing

9. cryptography --> Encryption and decryption operations
   Useful Methods:
   - Fernet() --> Symmetric encryption
   - RSA keys --> Asymmetric encryption
   - hashing functions --> Create password hashes
   Use case: Payload encryption, credential cracking, secure communication

10. hashlib --> Hashing library for password cracking
    Useful Methods:
    - hashlib.md5/sha1/sha256() --> Create hashes
    - .hexdigest() --> Get hex representation
    Use case: Rainbow tables, brute force, credential validation

11. re (Regular Expressions) --> Pattern matching
    Useful Methods:
    - re.findall(pattern, text) --> Extract matching patterns
    - re.sub(pattern, replacement, text) --> Replace patterns
    Use case: Data extraction, log analysis, payload generation

12. selenium --> Web browser automation
    Useful Methods:
    - webdriver.Chrome/Firefox() --> Control browser
    - driver.find_element() --> Locate elements
    - driver.execute_script() --> Run JavaScript
    Use case: Bypassing JavaScript validation, automation of complex exploits

13. pwntools --> CTF and exploitation framework
    Useful Methods:
    - process() --> Execute local binaries
    - remote() --> Connect to remote services
    - cyclic() --> Generate cyclic patterns for buffer overflows
    - packed() --> Pack/unpack data for exploits
    Use case: Binary exploitation, ROP gadget chains

14. metasploit-framework (or invoke via subprocess) --> Exploitation framework
    Use case: Rapid exploitation, payload generation, post-exploitation

15. pycryptodome --> Enhanced cryptography library
    Useful Methods:
    - AES encryption/decryption
    - RSA operations
    - DES/3DES algorithms
    Use case: Bypassing encryption, payload obfuscation

16. telnetlib --> Telnet protocol client
    Useful Methods:
    - Telnet() --> Connect to Telnet servers
    - read_until() --> Read server responses
    - write() --> Send commands
    Use case: Legacy system exploitation, brute force attacks

17. ftplib --> FTP protocol operations
    Useful Methods:
    - FTP() --> Connect to FTP servers
    - login() --> Authenticate
    - retrbinary() --> Download files
    Use case: FTP exploitation, credential brute force

18. imaplib/smtplib --> Email protocol operations
    Useful Methods:
    - login() --> Authenticate to email servers
    - select() --> Access mailboxes
    - search() --> Find emails
    Use case: Email enumeration, social engineering automation

19. dnspython --> DNS operations
    Useful Methods:
    - dns.resolver.query() --> DNS lookups
    - dns.zone.from_xfr() --> Zone transfers
    Use case: Reconnaissance, DNS spoofing, subdomain enumeration

20. pillow (PIL) --> Image manipulation
    Useful Methods:
    - Image.open() --> Load images
    - Image manipulation for steganography
    Use case: Hiding malware in images, screenshot capture