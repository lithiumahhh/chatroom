# client chat room. the client needs to send the messages

import socket
import select
import errno
import sys

header_len = 10
IP = "127.0.0.1"
port = 21435

username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, port))
client_socket.setblocking(False)

username = username.encode("utf-8")
username_header = f"{len(username):<{header_len}}".encode("utf-8")
client_socket.send(username_header + username)

while True: 
    message = input(f"{username} > ")

    if message: 
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {header_len}}".encode("utf-8")
        client_socket.send(message_header + message)
    
    try: 
        while True: 
            username_header = client_socket.recv(header_len)
            if not len(username_header): 
                print("Connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode("utf-8"))
            username = client_socket.recv(username_length).decode("utf-8")

            message_header = client_socket.recv(header_len)
            message_length = int(message_header.decode("utf-8"))
            message = client_socket.recv(message_length).decode("utf-8")

            print(f"{username} > {message}")
    
    except IOError as e: 
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK: 
            print('reading error', str(e))
            sys.exit()
        continue
    
    except Exception as e: 
        print('General error', str(e))
        sys.exit()
