import socket
import threading
RISKY = [21,22,3306,3389,445]
def port_scan(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, port))
        print(f"Port {port} is open")
        

        if port in RISKY:
            print(f"Port {port} is risky")
        s.close()

    except Exception as e:
        print("Port closed")

ip = input("Enter the IP address: ")
ports = list(map(int, input("Enter the ports: ").split()))


threads = []

for port in ports:
    t = threading.Thread(target=port_scan,args=(ip, port))
    threads.append(t)
    t.start()

for thread in threads:
    thread.join()









