"""
Advanced utilities for port scanning and vulnerability assessment
"""

import socket
import ssl
import sys

class BannerGrabber:
    """Extract service banners for identification."""
    
    @staticmethod
    def grab_banner(host, port, timeout=3):
        """Attempt to grab service banner."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            return banner if banner else None
        except Exception as e:
            return None
    
    @staticmethod
    def grab_https_cert(host, port, timeout=3):
        """Extract SSL/TLS certificate information."""
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((host, port), timeout=timeout) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    return {
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'version': ssock.version(),
                        'cipher': ssock.cipher(),
                    }
        except Exception as e:
            return None


class PortDescription:
    """Detailed descriptions of common ports and services."""
    
    PORT_INFO = {
        21: {
            "service": "FTP",
            "description": "File Transfer Protocol - unencrypted file transfer",
            "encrypted": False,
            "risk_level": "High",
            "recommendation": "Use SFTP (SSH File Transfer) instead"
        },
        22: {
            "service": "SSH",
            "description": "Secure Shell - encrypted remote access",
            "encrypted": True,
            "risk_level": "Low",
            "recommendation": "Use strong key pairs, disable password auth"
        },
        23: {
            "service": "Telnet",
            "description": "Unencrypted remote access protocol",
            "encrypted": False,
            "risk_level": "Critical",
            "recommendation": "Never use in production - use SSH instead"
        },
        25: {
            "service": "SMTP",
            "description": "Simple Mail Transfer Protocol",
            "encrypted": False,
            "risk_level": "Medium",
            "recommendation": "Use SMTPS or secure relay"
        },
        53: {
            "service": "DNS",
            "description": "Domain Name System - name resolution",
            "encrypted": False,
            "risk_level": "Medium",
            "recommendation": "Implement DNSSEC and restrict zone transfers"
        },
        80: {
            "service": "HTTP",
            "description": "HyperText Transfer Protocol - unencrypted web",
            "encrypted": False,
            "risk_level": "High",
            "recommendation": "Use HTTPS exclusively"
        },
        443: {
            "service": "HTTPS",
            "description": "HTTP Secure - encrypted web",
            "encrypted": True,
            "risk_level": "Low",
            "recommendation": "Ensure valid SSL/TLS certificates"
        },
        445: {
            "service": "SMB",
            "description": "Server Message Block - Windows file sharing",
            "encrypted": False,
            "risk_level": "Critical",
            "recommendation": "Restrict access with firewall"
        },
        3306: {
            "service": "MySQL",
            "description": "MySQL Database Server",
            "encrypted": False,
            "risk_level": "Critical",
            "recommendation": "Never expose to internet, use strong auth"
        },
        3389: {
            "service": "RDP",
            "description": "Remote Desktop Protocol - Windows remote access",
            "encrypted": True,
            "risk_level": "High",
            "recommendation": "Use VPN, disable if not needed"
        },
        5432: {
            "service": "PostgreSQL",
            "description": "PostgreSQL Database Server",
            "encrypted": False,
            "risk_level": "Critical",
            "recommendation": "Restrict network access strictly"
        },
        8080: {
            "service": "HTTP-Alt",
            "description": "Alternative HTTP port",
            "encrypted": False,
            "risk_level": "Medium",
            "recommendation": "Use HTTPS encryption"
        },
    }
    
    @classmethod
    def get_info(cls, port):
        """Get detailed port information."""
        return cls.PORT_INFO.get(port, {
            "service": "Unknown",
            "description": "Service not in database",
            "risk_level": "Unknown",
            "recommendation": "Research service manually"
        })


class SecurityRecommendations:
    """Security hardening recommendations based on scan results."""
    
    @staticmethod
    def get_firewall_rules(open_ports):
        """Generate firewall rule recommendations."""
        rules = []
        for port in open_ports:
            if port in [22, 443]:  # Safe ports
                rules.append(f"ALLOW TCP port {port} (SSH/HTTPS)")
            else:
                rules.append(f"DENY TCP port {port} (or restrict to specific IPs)")
        return rules
    
    @staticmethod
    def get_hardening_steps():
        """General hardening recommendations."""
        return [
            "1. Update all software to latest patches",
            "2. Disable unnecessary services",
            "3. Implement host-based firewall",
            "4. Use strong authentication (keys > passwords)",
            "5. Enable encryption for all protocols",
            "6. Regular security audits",
            "7. Monitor logs for suspicious activity",
            "8. Implement network segmentation",
            "9. Use VPN for remote access",
            "10. Regular backups and disaster recovery plan"
        ]


if __name__ == "__main__":
    # Example usage
    print("Banner Grabber Example:")
    banner = BannerGrabber.grab_banner("example.com", 80)
    print(f"Banner from example.com:80 = {banner}")
    
    print("\nPort Information Example:")
    info = PortDescription.get_info(22)
    print(f"Port 22 Info: {info}")
