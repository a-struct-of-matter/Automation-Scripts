hosts = {
    "192.168.1.10": [22, 80],
    "192.168.1.20": [21, 3306],
    "192.168.1.30": [443]
}


risky = [21,22,3306]

for host, ports in hosts.items():
    for port in ports:
        if port in risky:
            print(f"Host {host} has risky port {port} open!")
