import socket
import os
import math
import hashlib


def main():

    serverAddressPort   = ("127.0.0.1", 6666)
    bufferSize          = 1024

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    while(True):
        fileName = input("Digite o nome do arquivo > ")

        try:
            filesize = os.stat(fileName).st_size
            bFilesize = filesize.to_bytes(4, 'big')

            nameSize = len(fileName)
            bNameSize = nameSize.to_bytes(1, 'big')

        except:
            print("Arquivo não encontrado")
            continue
        
        
        UDPClientSocket.sendto(bNameSize + fileName.encode('utf-8') + bFilesize, serverAddressPort)

        if filesize <= bufferSize:
            file = open(fileName, 'rb')
            checksum = hashlib.sha1(file.read()).hexdigest()
            
            file.seek(0) # Volta para o começo do arquivo
            data = file.read(bufferSize)  
            file.close()

            UDPClientSocket.sendto(data, serverAddressPort)
        
        else:  
            pacotes = filesize/bufferSize
            pacote = 0
            file = open(fileName, 'rb')
            checksum = hashlib.sha1(file.read()).hexdigest()
            
            file.seek(0) # Volta para o começo do arquivo
            print("checksum: ", checksum)

            while pacote < int(math.ceil(pacotes)):
                data = file.read(bufferSize)
                print(' ',end='')
                UDPClientSocket.sendto(data, serverAddressPort)
                pacote += 1
            file.close()

        UDPClientSocket.sendto(checksum.encode('utf-8'), serverAddressPort)
        msgFromServer, addr = UDPClientSocket.recvfrom(bufferSize)
        print(msgFromServer.decode('utf-8'))


main()