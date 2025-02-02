import requests
import socket
import subprocess
import sys


RELEASE_NAME = "relis-my-service"
NAMESPACE = "default"
HOSTS = ["192.168.1.32", "20.103.44.21"]
PORTS = [80, 443, 8080]


'''checking availability Http/Https'''
def check_http_https(host, port):
    url = f"http://{host}:{port}" if port == 80 else f"https://{host}:{port}"
    try:
        response = requests.get(url, timeout=10, verify=False)

        if response.status_code == 200:
            print(f" [Ok] {url} available")
            return True
        else:
            print(f" [Error] {url} return {response.status_code}")
            return False
        
    except requests.exceptions.RequestException as e:
        print(f" [Error] error connection {url}: {e}")
        return False


'''checking availability Http/Https'''
def check_tcp_port(host, port):
    try:
        with socket.create_connection((host, port), timeout=5):
            print(f" [Ok] TCP-порт {host}:{port} available")
            return True
        
    except socket.error as e:
        print(f" [Error] error connection TCP {port} {host}: {e}")
        return False


'''checking status Helm-release'''
def check_helm_status():
    try:
        result = subprocess.run(["helm", "status", RELEASE_NAME, "-n", NAMESPACE], capture_output=True, text=True, check=True)
        print(f" [Ok] Helm-release '{RELEASE_NAME}' active:\n{result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[Error] Helm-release '{RELEASE_NAME}' error status:\n{e.stdout}")
        return False


'''rollback Helm-release'''
def rollback_helm():
    print("progress rollback")
    try:
        subprocess.run(["helm", "rollback", RELEASE_NAME, "1", "-n", NAMESPACE], check=True)

        print(" [Ok] Rollback of the release was completed successfully")

    except subprocess.CalledProcessError as e:
        print(f" [Error] Rollback of the release failed:\n{e.stdout}")

    errors = 0


    print("check  availability of services")
    for host in HOSTS:
        for port in PORTS:
            if port in [80, 443]:
                if not check_http_https(host, port):
                    errors += 1
            else:
                if not check_tcp_port(host, port):
                    errors += 1


    print("check status helm-release")
    if not check_helm_status():
        errors += 1


    if errors > 0:
        print(f"[Error] {errors} error, performing a rollback")
        rollback_helm()
        sys.exit(1)
    
    print("[Ok] Deployment was successful ")