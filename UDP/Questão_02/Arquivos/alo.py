from fileinput import filename
import socket
import os
import math

def main():

    serverAddressPort   = ("127.0.0.1", 6666)
    bufferSize          = 1024

    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    while(True):
        fileName = input("Digite o nome do arquivo > ")

        try:
            filesize = os.stat(fileName).st_size
            print("Tamanho do arquivo: ", filesize)
            bFilesize = filesize.to_bytes(4, 'big')
            print("Tamanho do arquivo em bytes: ", bFilesize)

            nameSize = len(fileName)
            print("Tamanho do nome do arquivo: ", nameSize)
            bNameSize = nameSize.to_bytes(1, 'big')
            print("Tamanho do nome do arquivo em bytes: ", bNameSize)

        except:
            print("Arquivo não encontrado")
            continue
        
        
        UDPClientSocket.sendto(bNameSize + fileName.encode('utf-8') + bFilesize, serverAddressPort)

        if filesize <= 1024:
            with open(fileName, 'rb') as file: # Abre o arquivo
                data = file.read(1024)  

            UDPClientSocket.sendto(data, serverAddressPort)
        
        else:  
            pacotes = filesize/1024
            print("Pacotes: ", int(math.ceil(pacotes)))
            pacote = 0
            file = open(fileName, 'wb')

            while pacote < int(math.ceil(pacotes)):
                data = file.read(1024)
                print("pacote:", pacote, "data:", data)
                print(' ',end='')
                UDPClientSocket.sendto(data, serverAddressPort)
                pacote += 1
                print("pacote:\n\n", pacote, "data:", data, "\n\n")


        msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    msg = "Message from Server {}".format(msgFromServer[0])
    print(msg)

main()