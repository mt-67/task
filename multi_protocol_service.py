from flask import Flask
import socket
import threading


app = Flask(__name__)


# HTTP Endpoint
@app.route('/')
def home():
    return "Hello, service!"


'''creates and manages a TCP server'''
def start_tcp_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket

    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(10) #max queue

    print(f"TCP server {port}")


    '''awaiting connection from the user'''
    while True:
        user_socket, user_address = server_socket.accept() #accepts connection, returns socket and address

        print(f"Connection from {user_address}") #connection information
        user_socket.sendall(b"Hello from TCP server")

        user_socket.close()


'''running TCP servers in separate threads'''
def start_tcp_servers():
    tcp_ports = [8080, 9000]

    for port in tcp_ports:
        threading.Thread(target=start_tcp_server, args=(port,), daemon=True).start()


if name == 'main':
    start_tcp_servers()  #start TCP-servers

    app.run(host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))