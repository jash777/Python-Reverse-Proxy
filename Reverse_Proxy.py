from socket import socket
import socket
import re

def waf_filter(request):
    # Define a list of rules
    request = request.decode("utf-8")
    rules = [
        r"DROP TABLE",
        r"DELETE FROM",
        r"INSERT INTO",
        r"xp_cmdshell",
        r"UNION SELECT",
        r"src='javascript:",
        r"src=javascript:",
        r"onmouseover=",
        r"onfocus=",
        r"onerror=",
    ]
    # Check if the request matches any of the rules
    for rule in rules:
        if re.search(rule, request):
            # If the request matches a rule, return False
            print('Detected')
            return False
    # If the request does not match any of the rules, return True
    print("Pass")
    return True
LOCAL_IP = '127.0.0.1'
LOCAL_PORT = 8080
# # Remote IP and port of the server to forward requests to
REMOTE_IP = '192.168.1.12'
REMOTE_PORT = 80
# Create a socket to listen for incoming connections
local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local_socket.bind((LOCAL_IP, LOCAL_PORT))
local_socket.listen()

while True:
    # Accept incoming connections
    client_socket, client_address = local_socket.accept()
    print('connection accepted')
    request = client_socket.recv(4096)
    if not waf_filter(request):
        client_socket.close()
        continue
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.connect((REMOTE_IP, REMOTE_PORT))
    print('server connect')
        # Forward the request from the client to the server
    server_socket.sendall(request)
    dbug_1 = server_socket.sendall(request)
    print('forwarding client requet to server')
    print(dbug_1)
        # Forward the response from the server back to the client
    response = b''
    while True:
        data = server_socket.recv(4096)
        if not data:
            break
        response += data
    client_socket.sendall(response)
    print('forwarding server response back to clinet')
    
        # Close the sockets
    client_socket.close()
    server_socket.close()
    print("Proxy Started!")
