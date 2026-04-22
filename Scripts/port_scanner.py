import threading
import socket


semaphore = threading.Semaphore(5)

def scan_ports(ip, port):
    
    with semaphore:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        
        try:
            s.connect((ip, port))
            print(f"Port {port} is open")
        
        except Exception as e:
            pass
        finally:
            s.close()

ip = input("Enter the IP in correct format: ")
print("Scanning Ports...Can take a while!")
threads = []

for port in range(1,101):
    t = threading.Thread(target=scan_ports, args=(ip, port))
    threads.append(t)
    t.start()

for thread in threads:
    thread.join()
print("Scan Complete!")