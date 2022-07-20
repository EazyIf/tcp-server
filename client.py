import socket
import threading
import colorama
from art import tprint
import os 
file1 = "D:\\vs code projects\\Python\\coo1\\rick-roll.mp3"
FORMAT = "utf-8"

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

colorama.init()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('127.0.0.1',8022))

CONNECTION_OPEN = True

def receive():
    global CONNECTION_OPEN
    while CONNECTION_OPEN:
        try:
            response = server.recv(1024)
        except ConnectionAbortedError:
            CONNECTION_OPEN = False
            break
        
        # remove last line
        print(ERASE_LINE, end='\r')
        print(response.decode())
        print('Enter your message: ', end='')
    server.close()

def dababy_send():
    global CONNECTION_OPEN
    while CONNECTION_OPEN:
        try:
            user_input = input('Enter your message: ') 
        except EOFError:
            user_input = '/exit'
            
        if user_input == '/exit':
            server.close()
            CONNECTION_OPEN = False
            break
        # if user_input == '/dababy':
        #     file = open("D:\\vs code projects\\Python\\coo1\\rick-roll.mp3", "r")
        #     data = file.read()
        #     client.send("rick_roll.mp3".encode(FORMAT))
            # server.send("D:\\vs code projects\\Python\\coo1\\rick-roll.mp3".encode())
            # # msg = server.recv(SIZE).decode(FORMAT)
            # # print(f"[SERVER]: {msg}")
            # server.send(data.encode())
            # # msg = server.recv(SIZE).decode(FORMAT)
            # # print(f"[SERVER]: {msg}")


            
        print(CURSOR_UP_ONE + ERASE_LINE, end='\r')
        server.send(user_input.encode())

if __name__ == '__main__':
    tprint(text='chat.py', font='slant')
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    send_thread = threading.Thread(target=dababy_send)
    send_thread.start()
    