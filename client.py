import socket
import threading
import tkinter as tk
from tkinter import messagebox

BACKGROUND_COLOR = '#FCFCFC'
BACKGROUND_LIGHT = '#EEEEEE'
GRAY = '#2E2C2C'
WHITE = '#FFFFFF'
BLACK = '#000000'
BLACK_DISABLED = '#151515'
PRIMARY = '#0BCA0B'
PRIMARY_DISABLED = '#3FFF3F'
FONT = ('Helvetica', 14)
FONT_BOLD = ('Helvetica', 14, 'bold')
FONT_SMALL = ('Helvetica', 10)
PADDING = 14

HOST = 'localhost'
PORT = 1234

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def addMessage(message):
    messageBox.config(state=tk.NORMAL)
    messageBox.insert(tk.END, message + '\n')
    messageBox.config(state=tk.DISABLED)

def connect():
    try:
        clientSocket.connect((HOST, PORT))
        addMessage('Successfully connected to server')
    except:
        messagebox.showerror('Unable to connect to server', f'Unable to connect to server {HOST} {PORT}')

    username = usernameTextbox.get()
    if username != '':
        clientSocket.send(username.encode())
    else:
        messagebox.showerror('Invalid Username', 'Username cant be empty')

    threading.Thread(target=listenForMessagesFromServer, args=(clientSocket, )).start()

    usernameTextbox.config(state=tk.DISABLED, cursor='arrow')
    usernameLabel.config(state=tk.DISABLED)
    usernameButton.config(state=tk.DISABLED, bg=PRIMARY_DISABLED, fg=BLACK_DISABLED)
    messageTextbox.config(state=tk.NORMAL)
    messageLabel.config(state=tk.NORMAL)
    messageButton.config(state=tk.NORMAL, bg=PRIMARY, fg=BLACK)


def sendMessage():
    message = messageTextbox.get()
    if message != '':
        clientSocket.send(message.encode())
        messageTextbox.delete(0, len(message))
    else:
        messagebox.showerror('Empty message', 'Message cant be empty')

def listenForMessagesFromServer(clientSocket):
    while True:
        message = clientSocket.recv(2048).decode('utf-8')
        if message != '':
            username = message.split(':')[0]
            content = message.split(':')[1]
            
            addMessage(f'{username}: {content}')
        else:
            messagebox.showerror('Message Recieve Error', 'Message recevied from client is empty')

root = tk.Tk()
root.geometry('414x696')
root.title('Chatlo')
root.resizable(False, False)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

headerFrame = tk.Frame(root, width=414, height=74, bg=WHITE, padx=PADDING, pady=PADDING)
headerFrame.grid(row=0, column=0, sticky=tk.NSEW)

bodyFrame = tk.Frame(root, width=414, height=544, bg=BACKGROUND_COLOR)
bodyFrame.grid(row=1, column=0, sticky=tk.NSEW)

footerFrame = tk.Frame(root, width=414, height=74, bg=WHITE, padx=PADDING, pady=PADDING)
footerFrame.grid(row=2, column=0, sticky=tk.NSEW)

usernameLabel = tk.Label(headerFrame, text='Username:', font=FONT, fg=GRAY, bg=WHITE)
usernameLabel.pack(side=tk.LEFT, fill='y')

usernameTextbox = tk.Entry(headerFrame, font=FONT, bg=BACKGROUND_LIGHT, fg=BLACK, width=19)
usernameTextbox.pack(side=tk.LEFT, padx=(2, 8), fill='y')

usernameButton = tk.Button(headerFrame, font=FONT_BOLD, text='Join', bg=PRIMARY, fg=BLACK, command=connect)
usernameButton.pack(side=tk.RIGHT, fill='y', padx=8)

messageLabel = tk.Label(footerFrame, text='Message:', font=FONT, fg=GRAY, bg=BACKGROUND_COLOR)
messageLabel.config(state=tk.DISABLED)
messageLabel.pack(side=tk.LEFT, fill='y')

messageTextbox = tk.Entry(footerFrame, font=FONT, bg=BACKGROUND_LIGHT, fg=BLACK, width=19)
messageTextbox.config(state=tk.DISABLED)
messageTextbox.pack(side=tk.LEFT, padx=(2, 8), fill='y')

messageButton = tk.Button(footerFrame, font=FONT_BOLD, text='Send', bg=PRIMARY_DISABLED, fg=BLACK_DISABLED, command=sendMessage)
messageButton.config(state=tk.DISABLED)
messageButton.pack(side=tk.RIGHT, fill='y', padx=8)

messageBox = tk.Text(bodyFrame, font=FONT_SMALL, bg=WHITE, fg='black', width=56, height=34, padx=PADDING, pady=PADDING, cursor='arrow')
messageBox.config(state=tk.DISABLED)
messageBox.pack(side=tk.TOP)

def main():
    root.mainloop()

if __name__ == '__main__':
    main()