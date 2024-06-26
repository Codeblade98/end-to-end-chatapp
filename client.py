import socket
import threading

host = '127.0.0.1' #local host
port = 55555 # generally dont choose between 0-10k, 80 for http

nickname = input("Enter you nick: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message=='Nick':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occured!!")
            client.close()
            break

def write():
    while True:
        message = f"{nickname}: {input('')}"
        if message.startswith('\\chat'):
            # Extract the actual message intended for the chatbot
            chat_message = message[len('\\chat'):].strip()
            
            # Send command to server to initiate chat with chatbot
            client.send(f"\\chat{chat_message}".encode('ascii'))
        else:
            # Regular chat message to send to server
            client.send(message.encode('ascii'))

print("Use \\chat to chat with chatbot and \\chatp to chat privately with chatbot\n")
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()