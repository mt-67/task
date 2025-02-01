import socket
import requests
import subprocess


hosts = ["192.168.1.32", "20.103.44.21"]

ports = [80, 443, 8080]

release_name = "relis-my-service"

namespace = "default"


'''Check Http/Https ports'''
def check_http_https(host, port):
    url = f"http://{host}:{port}" if port == 80 else f"https://{host}:{port}"
    try:
        response = requests.get(url, timeout=10, verify=False)  # verify is ignor ssl

        if response.status_code == 200:
            print(f"[Ok] {url} available")
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
        with socket.create_connection((host, port), timeout=10):
            print(f"[Ok] Custom TCP {host}:{port} available")
            return True
        
    except socket.error as e:
        print(f"[Error] Connection error TCP {port} {host} {e}")
        return False


'''Check status Helm-release'''
def check_helm_status():
    try:
        result = subprocess.run(
            ['helm', 'status', release_name, '--namespace', namespace],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True)
        
        output = result.stdout.decode('utf-8')
        if "Status: deployed" in output:
            print(f"[OK] Helm-release {release_name} successfully deployed")
            return True
        else:
            print(f"[Error] Helm-release {release_name} not in the 'deployed' state")
            return False
        
    except subprocess.CalledProcessError as e:
        print(f"[Error] Error checking the Helm release: {e}")
        return False


'''rollback Helm-release'''
def rollback_helm_release():
    try:
        subprocess.run(
            ['helm', 'rollback', release_name, '1', '--namespace', namespace],
            check=True)
        
        print(f"[Rollback] Rolling back the Helm release {release_name} available.")

    except subprocess.CalledProcessError as e:
        print(f"[Error] Error rolling back the Helm release: {e}")


'''Check deploy'''
def main():
    all_ports_ok = True


    '''Check all ports and hosts'''
    for host in hosts:
        for port in ports:
            if port in [80, 443]:
                if not check_http_https(host, port):
                    all_ports_ok = False
            else:
                if not check_tcp_port(host, port):
                    all_ports_ok = False

    helm_ok = check_helm_status() #check Helm-release


    '''rollback deploy'''
    if not all_ports_ok or not helm_ok:
        print("[Error] Problems are found, we are performing a rollback")
        rollback_helm_release()
    else:
        print("[Success] The deployment is successful, all services are working")

main()