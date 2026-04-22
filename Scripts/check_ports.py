import socket as soc

s = soc.socket()


risky = [21,22,3306,443,3389]

for port in risky:
    try:
        s.connect(("192.168.29.237", port))
        print(f"Port {port} is open and risky!")
    except Exception as e:
        print(f"Port {port} is closed.")
s.close()
