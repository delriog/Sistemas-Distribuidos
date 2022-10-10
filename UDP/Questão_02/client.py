'''

    Programação com sockets UDP

    Descrição: Sistema de upload de arquivos via UDP

    Um servidor UDP que recebe as partes dos arquivos (1024 bytes), verifica ao final a integridade via um checksum (SHA-1) 
    e armazena o arquivo em uma pasta padrão.

    Autores: Caio José Cintra, Guilherme Del Rio
    Data de criação: 24/09/2022
    Data de modificação: 27/09/2022

'''

import socket
import os
import math
import hashlib


def main():

    # IP da máquina conectada, por padrão 127.0.0.1 e porta usada para conexão
    serverAddressPort   = ("127.0.0.1", 6666)

    # Tamanho de buffer
    bufferSize          = 1024

    # Criação de socket
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Laço principal de execução
    while(True):
        # Usuário digita nome do arquivo
        fileName = input("Digite o nome do arquivo > ")

        try:
            # Procura arquivo com nome inserido
            filesize = os.stat(fileName).st_size                # Pega o tamanho do arquivo
            bFilesize = filesize.to_bytes(4, 'big')

            nameSize = len(fileName)                            # Pega o tamanho do nome do arquivo
            bNameSize = nameSize.to_bytes(1, 'big')

        except:
            # Caso não encontre, retorna erro
            print("Arquivo não encontrado")
            continue
        
        # Envia os dados para o servidor: tamanho do nome, nome e tamanho do arquivo
        UDPClientSocket.sendto(bNameSize + fileName.encode('utf-8') + bFilesize, serverAddressPort)

        # Verififica se o arquivo é menor que o buffer
        if filesize <= bufferSize:
            # Caso seja, ele abre o arquivo
            file = open(fileName, 'rb')
            # Obtêm o checksum do arquivo
            checksum = hashlib.sha1(file.read()).hexdigest()
            
            file.seek(0)                    # Volta para o começo do arquivo
            data = file.read(bufferSize)    # Lê o arquivo inteiro
            file.close()                    # Fecha o arquivo

            # Envia o arquivo
            UDPClientSocket.sendto(data, serverAddressPort)
        
        else:
            # Caso o arquivo seja maior que o buffer

            pacotes = filesize/bufferSize                       # Divide o tamanho do arquivo pelo do buffer para encontrar o total de pacotes
            pacote = 0                                          # Variável de controle
            file = open(fileName, 'rb')                         # Abre o arquivo
            checksum = hashlib.sha1(file.read()).hexdigest()    # Obtêm o checksum do arquivo inteiro
            
            file.seek(0)  # Volta para o começo do arquivo
            print("checksum: ", checksum)

            # Enquanto a variável de controle for menor que a quantidade de pacotes
            while pacote < int(math.ceil(pacotes)):
                data = file.read(bufferSize)            # Lê 1024 bytes do arquivo
                print(' ',end='')                       # print para não desorganizar os dados lidos
                
                # Envia dados para o servidor
                UDPClientSocket.sendto(data, serverAddressPort)
                pacote += 1
            file.close()

        # Envia o checksum para o servidor
        UDPClientSocket.sendto(checksum.encode('utf-8'), serverAddressPort)

        # Recebe a mensagem de resposta do servidor
        msgFromServer, addr = UDPClientSocket.recvfrom(bufferSize)
        print(msgFromServer.decode('utf-8'))


main()