import socket
import requests


HOSTS = ["108.141.128.223", "20.61.89.128"]

PORTS = [80, 443, 8080]

"""Checking the availability of Http/Https ports"""
def check_http_https(host, port):
    url = f"http://{host}:{port}" if port == 80 else f"https://{host}:{port}"
    try:
        response = requests.get(url, timeout=10, verify=False)  # verify is ignor ssl

        if response.status_code == 200:
            print(f" [Ok] {url} available")
            return True
        else:
            print(f"[Error] {url} status code {response.status_code}")
            return False
        
    except requests.exceptions.RequestException as e:
        print(f"[Error] Connection error {url}: {e}")
        return False


'''Check TCP port'''
def check_tcp_port(host, port):
    try:
        with socket.create_connection((host, port), timeout=5):
            print(f"[Ok] TCP-port {host}:{port} available")
            return True
        
    except socket.error as e:
        print(f" [Error] Connection error TCP {port} {host} {e}")
        return False


for host in HOSTS:
    print(f"Check  {host}")

    for port in PORTS:
        if port in [80, 443]:
            check_http_https(host, port)
        else:
            check_tcp_port(host, port)