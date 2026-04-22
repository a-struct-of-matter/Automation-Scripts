import google.generativeai as genai
import os
from typing import Optional, Dict, List


class GeminiAnalyzer:
    """AI analyzer for security insights using Gemini."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini analyzer with API key."""
        if api_key is None:
            api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError(
                "Gemini API key not found. Please provide it via:\n"
                "1. Environment variable: GEMINI_API_KEY\n"
                "2. Pass directly to this function\n"
                "Get your free API key from: https://aistudio.google.com/apikey"
            )
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash')
        self.chat = self.model.start_chat()
    
    def analyze_port(self, port: int, service: str, known_vulnerabilities: List[str]) -> str:
        """Get AI analysis for a specific port/service."""
        prompt = f"""
        You are a cybersecurity expert. Provide a brief but comprehensive security analysis for:
        
        Port: {port}
        Service: {service}
        Known Vulnerabilities:
        {chr(10).join(f"- {v}" for v in known_vulnerabilities)}
        
        Please provide:
        1. Risk Assessment (Critical/High/Medium/Low)
        2. Key Security Concerns (2-3 points)
        3. Immediate Actions (quick wins)
        4. Long-term Hardening
        
        Keep the response concise and actionable.
        """
        
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Error analyzing with AI: {str(e)}"
    
    def get_remediation(self, service: str, vulnerability: str) -> str:
        """Get specific remediation steps for a vulnerability."""
        prompt = f"""
        Provide step-by-step remediation for this security vulnerability:
        
        Service: {service}
        Vulnerability: {vulnerability}
        
        Please provide:
        1. Immediate Fix (if available)
        2. Configuration Changes
        3. Verification Steps
        4. Testing
        
        Be specific and technical. Assume Linux/Windows server context.
        """
        
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Error getting remediation: {str(e)}"
    
    def generate_security_report(self, host: str, open_ports: Dict[int, str]) -> str:
        """Generate comprehensive security report for all open ports."""
        ports_list = "\n".join([f"- Port {p}: {s}" for p, s in open_ports.items()])
        
        prompt = f"""
        Create a professional cybersecurity assessment report for:
        
        Target Host: {host}
        Open Ports:
        {ports_list}
        
        Please provide:
        1. Executive Summary (risk level, critical findings)
        2. Detailed Findings (by port)
        3. Prioritized Recommendations
        4. Estimated Risk Score (1-10)
        5. Compliance Considerations
        
        Format as a professional report suitable for stakeholders.
        """
        
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Error generating report: {str(e)}"
    
    def ask_security_question(self, question: str) -> str:
        """Interactive Q&A for security questions."""
        try:
            response = self.chat.send_message(question)
            return response.text
        except Exception as e:
            return f"Error answering question: {str(e)}"
    
    def get_cve_info(self, service: str, cve_id: Optional[str] = None) -> str:
        """Get information about CVEs for a service."""
        if cve_id:
            prompt = f"Provide details about {cve_id} for {service}. Include: severity, impact, fix."
        else:
            prompt = f"""
            List the top 5 current CVEs affecting {service}:
            For each include: CVE ID, CVSS Score, Impact, and mitigation.
            """
        
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Error getting CVE info: {str(e)}"
    
    def get_hardening_guide(self, service: str) -> str:
        """Get a complete hardening guide for a service."""
        prompt = f"""
        Provide a comprehensive hardening guide for {service}:
        
        Include:
        1. Pre-requisites
        2. Security Configuration Steps
        3. Network Hardening
        4. Monitoring & Logging Setup
        5. Testing & Verification
        6. Compliance Alignment (CIS, NIST)
        
        Be detailed and practical.
        """
        
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Error generating hardening guide: {str(e)}"
    
    def compare_services(self, services: List[str]) -> str:
        """Compare security posture of different services."""
        services_list = ", ".join(services)
        prompt = f"""
        Compare the security characteristics of these services: {services_list}
        
        For each, provide:
        1. Security Rating (1-10)
        2. Main Vulnerabilities
        3. When to Use
        4. Secure Alternatives
        
        Format as a comparison table if possible.
        """
        
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Error comparing services: {str(e)}"


class AIInsightCache:
    """Cache AI insights to reduce API calls."""
    
    def __init__(self):
        self.cache = {}
    
    def get(self, key: str) -> Optional[str]:
        """Get cached insight."""
        return self.cache.get(key)
    
    def set(self, key: str, value: str):
        """Cache an insight."""
        self.cache[key] = value
    
    def clear(self):
        """Clear all cached insights."""
        self.cache.clear()


if __name__ == "__main__":
    # Test the analyzer
    try:
        analyzer = GeminiAnalyzer()
        response = analyzer.analyze_port(22, "SSH", ["Brute force attacks possible"])
        print(response)
    except Exception as e:
        print(f"Setup Error: {str(e)}")
