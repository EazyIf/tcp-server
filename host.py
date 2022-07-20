import socket
import select
import os
import logging
from sqlite3 import connect
from colorlog import ColoredFormatter
from art import tprint
FORMAT = "utf-8"


def init_logging():
    stream = logging.StreamHandler()
    stream.setFormatter(ColoredFormatter("%(log_color)s%(message)s%(reset)s"))

    log = logging.getLogger('pythonConfig')
    log.setLevel(logging.DEBUG)
    log.addHandler(stream)

    return log


MAX_MSG_LENGTH = 1024
SERVER_PORT = 8022
SERVER_IP = '0.0.0.0'


def main():
    log.info('Setting up server...')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    log.info(f'Success, your server ip is {socket.gethostbyname(socket.gethostname())}:{SERVER_PORT}')
    server_socket.listen()
    log.info('Listening for clients...')
    clients = []
    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + clients, [], [])
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                client_socket, client_address = current_socket.accept()
                log.info(f'--> Client {":".join([str(d) for d in client_address])} joined')
                clients.append(client_socket)
                continue
            
            try:
                data = current_socket.recv(MAX_MSG_LENGTH).decode()
            except ConnectionResetError:
                data = '/exit'
                
            if data == '/exit':
                close_connection(current_socket, clients)
                continue
            # if data == '/dababy':
            #     filename = file
            #     print(f"[RECV] Receiving the filename.")
            #     file = open(filename, "w")
            #     # conn.send("Filename received.".encode(FORMAT))
            #     # """ Receiving the file data from the client. """
            #     data.recv(1024).decode()
            #     print(f"[RECV] Receiving the file data.")
            #     file.write(data)
            #     # conn.send("File data received".encode(FORMAT))
            #     # data.open()
            
            log.info(f'New data from client {":".join([str(d) for d in current_socket.getpeername()])} - {data}')
            # send the data to all clients with ip of sender
            for client_socket in clients:
                client_socket.send(f'{":".join([str(d) for d in current_socket.getpeername()])}: {data}'.encode())


def close_connection(client, clients):
    log.info(msg=f'<-- Client {":".join([str(d) for d in client.getpeername()])} left')
    client.close()
    clients.remove(client)

log = init_logging()
tprint(text='server.py', font='slant')
main()
