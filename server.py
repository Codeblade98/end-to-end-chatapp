import threading
import socket
import chatbot
from datetime import datetime

host = '127.0.0.1' #local host
port = 55555 # generally dont choose between 0-10k, 80 for http

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    '''Send message to all clients connected to the server'''
    for client in clients:
        client.send(message)

def handle(client):
    '''Handling a single client'''
    while True:
        try:
            message=client.recv(1024) #receive 1024 bytes
            if message:
                message_str = message.decode('ascii').strip()
                broadcast(message)
            if '\\chat' in message_str:
                # Extract the actual message intended for the chatbot
                chat_message = message_str[len('\\chat'):].strip()
                
                session_id = nicknames[clients.index(client)] 

                try:# Invoke chatbot with the session_id and message
                    response = chatbot.chatbot("11", chat_message)
                    response = f"Chatbot: {response}"
                except:
                    print("An error occured!!")

                # Send response back to the client
                if '\\chatp' in message_str:
                    client.send(response.encode('ascii'))
                else:
                    broadcast(response.encode('ascii'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat".encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client,address = server.accept()
        print(f"Connected with {str(address)}")
        client.send('Nick'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname of client is {nickname}")
        broadcast(f"{nickname} joined the chat".encode('ascii'))
        client.send("Connected to the server".encode('ascii'))

        ## use a thread to make it run for all clients
        thread = threading.Thread(target=handle,args=(client,))
        thread.start()

print(f"Server started at {datetime.now()}")
receive()