# Port Scanner with AI Vulnerability Analysis

A Python-based port scanning tool that identifies open ports on target systems and provides AI-powered vulnerability analysis using Google's Gemini API.

## What It Does

This tool scans a target host for open ports, identifies the services running on those ports, and uses artificial intelligence to provide detailed vulnerability assessments and remediation recommendations. It's designed for learning cybersecurity concepts and authorized security testing.

## Features

- Multi-threaded port scanning for fast results
- Automatic service identification
- AI-powered vulnerability analysis
- Remediation step-by-step guides
- CVE information lookup
- Security hardening recommendations
- Interactive question and answer system
- JSON export of scan results
- Configuration management for API keys

## Requirements

- Python 3.6 or higher
- Google Gemini API key (free from https://aistudio.google.com/apikey)
- Internet connection for AI analysis

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Get your free Gemini API key from https://aistudio.google.com/apikey

4. Set your API key using one of these methods:
   - Environment variable: `$env:GEMINI_API_KEY = "your_key"`
   - Run setup wizard: `python setup.py`
   - Create config.json with your key

## Usage

Run the scanner with:
```
python port_scanner.py
```

The tool will guide you through an interactive menu where you can:
- Enter the target host (IP address or hostname)
- Choose to scan common ports or a custom range
- Set the number of threads for scanning speed
- Enable AI analysis for detailed insights
- Export results to JSON

## Example

```
Enter target host: 127.0.0.1
Select scan type: 1 (common ports)
Enter number of threads: 50
Use AI analysis: yes

[Scanning begins...]
[+] Port 22: SSH is OPEN
[+] Port 80: HTTP is OPEN
[+] Port 443: HTTPS is OPEN

[AI Analysis shows vulnerability details and recommendations]
```

## How It Works

1. The scanner connects to specified ports on the target system
2. For open ports, it identifies the service (SSH, HTTP, etc.)
3. It checks a database of known vulnerabilities for that service
4. If AI is enabled, it sends this information to Gemini for detailed analysis
5. Results are displayed with recommendations for improvement

## Important Legal Notice

Only use this tool on systems you own or have explicit written permission to test. Unauthorized scanning may be illegal. This tool is intended for educational purposes and authorized security assessments only.

## Project Structure

- `port_scanner.py` - Main scanning application
- `ai_analyzer.py` - AI integration with Gemini API
- `config.py` - Configuration and API key management
- `utilities.py` - Helper functions
- `setup.py` - Installation and setup wizard

## Configuration

The tool can be configured through:
- Command line prompts during execution
- Environment variables (GEMINI_API_KEY)
- config.json file

Default settings can be modified in config.py.

## Troubleshooting

If the scanner runs slowly, try using common ports mode instead of scanning the full range. To speed up scanning, increase the number of threads (up to 500).

If the AI features aren't working, verify your Gemini API key is correct and you have internet connectivity.

For connection errors, check that the target host is reachable from your network.

## Learning Resources

For more information about port scanning, vulnerabilities, and security concepts:
- Python documentation: https://docs.python.org
- OWASP: https://owasp.org
- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework

## Support

For questions or issues, check the START_HERE.md or QUICKSTART.md files for additional guidance.

## License

Educational use. See project files for full terms.
