import sys
from utils import risky_ports
if len(sys.argv) != 2:
    print("Usage: python main.py <port>")
    sys.exit(1)

port = int(sys.argv[1])
print("Checking port:", port)
if risky_ports(port):
    print(  f"Port {port} is considered risky.")
