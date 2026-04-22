risky = [21,22,3306]

res = {}

while True:
    port = input("Enter port number (or 'exit' to finish): ")

    if port.lower() == 'stop':
        break
    
    state = input("Enter state (open/closed): ").lower()
    res[port] = state

for port in res.keys():
    if int(port) in risky and res[port] == 'open':
        print(f"Port {port} is risky and open!")

