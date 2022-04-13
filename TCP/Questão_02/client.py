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

Solicitações:
----------------------------------------------------------------
|     0x01     |   0x01 a 0x04  |               | 0 a 255bytes |
----------------------------------------------------------------
| Message Type | Command Ident. | Filename Size |   Filename   |
----------------------------------------------------------------
"""

import socket
import os


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
        header = bytearray(4)
        header[0] = 1


        comando = input("Comando: ") 
        if len(comando.split()) > 1:
            operation = comando.split()[0].upper()
            fileName = comando.split()[1]
        else:
            operation = comando.upper()
        
        if operation == "ADDFILE": 
            header[1] = 1
            header[2] = len(fileName)
            arquivos = os.listdir()
            flag = False
            for nome in arquivos:
                if fileName == nome:
                    bFileName = bytearray(fileName.encode())
                    tamArquivo = (os.stat(fileName).st_size).to_bytes(4, "big")
                    flag = True

            if flag:
                client_socket.send(header + bFileName + tamArquivo)
                arquivo = open(fileName, 'rb') #abre o arquivo
                arquivo = arquivo.read() #le o arquivo
                client_socket.send(arquivo) #envia o arquivo
            


main()