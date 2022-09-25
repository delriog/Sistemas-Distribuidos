from fileinput import filename
import socket
import math

localIP     = "127.0.0.1"
localPort   = 6666
bufferSize  = 1024

def main():

    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))
    
    print("UDP server up and listening")

    # Listen for incoming datagrams
    while(True):

        msg, address = UDPServerSocket.recvfrom(bufferSize)
        print(msg)

        tamanhoNomeArquivo = int.from_bytes(msg[0:1], 'big')
        print("tamanho_nome_arquivo:", tamanhoNomeArquivo, end=' | ')

        nomeArquivo = msg[1:1+int(tamanhoNomeArquivo)].decode('utf-8')
        print("nomeArquivo:", nomeArquivo, end=' | ')

        tamanhoArquivo = int.from_bytes(msg[1+int(tamanhoNomeArquivo):], 'big')
        print("tamanhoArquivo:", tamanhoArquivo)

        pacotes = tamanhoArquivo/1024
        pacote = 0

        file2 = open('./Arquivos/' + nomeArquivo, 'wb+')

        while pacote < int(math.ceil(pacotes)):
                print("pacote:", pacote)            
                data, addr = UDPServerSocket.recvfrom(bufferSize)
                print("\n\npacote:", pacote, "data:", data, "\n\n")
                file2.write(data)
                pacote += 1
        file2.close()


main()