"""
    Programação com sockets TCP

    Descrição:aplicação com um servidor que gerencia um conjunto de arquivos remotos entre múltiplos usuários, usando os seguintes comandos:
    ADDFILE (1): adiciona um arquivo novo.
    DELETE (2): remove um arquivo existente.
    GETFILESLIST (3): retorna uma lista com o nome dos arquivos.
    GETFILE (4): faz download de um arquivo.

    Autores: Caio José Cintra, Guilherme Del Rio
    Data de criação: 09/04/2022
    Data de modificação: 12/04/2022

Respostas:
------------------------------------------------------
|     0x02     |   0x01 a 0x04  | 1-SUCCESS, 2-ERROR |
------------------------------------------------------
| Message Type | Command Ident. |     Status Code    |
------------------------------------------------------
"""

import threading 
import socket 
import os


host = ""
porta = 65432
addr = (host,porta) 

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
serv_socket.bind(addr)

def handler(ip, porta, socket):
    while True:
        header = bytearray(3)
        header[0] = 2

        # Recebe a mensagem
        msg = bytearray(socket.recv(1024))
        message_type = int(msg[0])
        command_ident = int(msg[1])
        filename_size = int(msg[2])
        file_name = msg[3:-(filename_size)].decode('utf-8')
        file = str(file_name)

        if command_ident == 1: 
            bFile_size = msg[-4:]

            file_size = int.from_bytes(bFile_size, byteorder='big')
            arquivo = socket.recv(file_size)
            with open("./arquivos/" + file, 'wb') as file:
                file.write(arquivo)





def main():
    vetorThreads = []

    while True:
        # Limite de 20 conexões
        serv_socket.listen(20)

        # Servidor escuta as conexões
        (socket , (ip,porta) ) = serv_socket.accept()
        print('Cliente: ', ip, 'conectado na porta: ', porta)

        # Cria e inicia uma thread para cada cliente que chega
        thread = threading.Thread(target=handler, args=(ip, porta, socket, ))
        thread.start()
        
        # Adiciona ao vetor de threads
        vetorThreads.append(thread)
        

main()