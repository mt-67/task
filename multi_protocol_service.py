from flask import Flask
import socket
import threading
from OpenSSL import SSL


app = Flask(__name__) #creates a Flask application for HTTPS

@app.route('/')
def hello_world():
    return 'Hello, My World!'


'''starts the HTTPS server'''
def start_https_server():
    context = ('cert.pem', 'key.pem')  
    app.run(host='0.0.0.0', port=443, ssl_context=context)


'''starts the TCP server'''
def start_tcp_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket

    server_socket.bind((host, port))
    server_socket.listen(10) #max queue

    print(f"TCP Server listening on {host}:{port}")
    

    '''awaiting connection from the user'''
    while True:
        user_socket, addr = server_socket.accept() #accepts connection, returns socket and address


        print(f"TCP connection from {addr}") #connection information
        user_socket.send(b"Hello, TCP user") # answer

        user_socket.close()


'''runs TCP servers in separate streams'''
def start_servers():
    ports = [8080] 

    for port in ports:
        threading.Thread(target=start_tcp_server, args=('0.0.0.0', port), daemon=True).start()


if __name__ == "main":
    start_servers() # runs TCP servers
    
    start_https_server() # Runs the Flask server with HTTPS