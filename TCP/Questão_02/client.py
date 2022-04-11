# echo-client.py
import socket
from sqlite3 import connect 

# IP da máquina conectada, por padrão 127.0.0.1
ip = "127.0.0.1"

# Porta usada para conexão
port = 65432

addr = (ip, port) 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect(addr)



def main():
    while True:
        comando = input("Comando: ") 
        # Envia mensagem
        client_socket.send(comando.encode("utf-8"))
        resposta = client_socket.recv(1024).decode("utf-8")

main()