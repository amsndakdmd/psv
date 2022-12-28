import socket
import threading

HOST = 'localhost'
PORT = 1234
MAX_CONNECTION_NUMBER = 5
clients = []

def listenForMessages(clientSocket, username):
    while True:
        message = clientSocket.recv(2048).decode('utf-8')
        if message != '':
            finalMessage = username + ':' + message
            sendMessageToAll(finalMessage)
        else:
            print(f'The message send from the client {username} is empty')

def sendMessageToClient(clientSocket, message):
    clientSocket.sendall(message.encode())
    
def sendMessageToAll(message):
    for client in clients:
        sendMessageToClient(client[1], message)

def clientHandle(clientSocket):
    while True:
        username = clientSocket.recv(2048).decode('utf-8')
        if username != '':
            clients.append((username, clientSocket))
            promptMessage = 'SERVER:' + f'{username} has joined the chat'
            sendMessageToAll(promptMessage)
            break
        else:  
            print('Client username is empty')
            
    threading.Thread(target=listenForMessages, args=(clientSocket, username, )).start()

def main():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serverSocket.bind((HOST, PORT))
        print(f'Server is running on {HOST} {PORT}')
    except:
        print(f'Unable to bind to host {HOST} and port {PORT}')

    serverSocket.listen(MAX_CONNECTION_NUMBER)

    while True:
        clientSocket, address = serverSocket.accept()
        print(f'Successfully connected to server {address[0]} {address[1]}')

        threading.Thread(target=clientHandle, args=(clientSocket, )).start()

if __name__ == '__main__':
    main()