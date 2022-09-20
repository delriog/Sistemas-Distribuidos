'''

    Programação com sockets TCP

    Descrição: Servidor que processa mensagens de múltiplos clientes com as seguintes operações disponíveis:

    CONNECT user,password: Conecta o usuário na servidor usando sua senha, em caso de sucesso deveolvendo SUCCESS e caso contrário devolvendo ERROR,
    enquanto o usuário não está conectado ele não pode executar comandos.
    PWD: Devolve o caminho corrente usando String UTF, separando diretórios por barra.
    CHDIR path: Altera o diretório atual para 'path', retornando SUCCESS caso seja bem sucedido e ERROR caso contrário.
    GETFILES: Devolve os arquivos do diretório atual no servidor.
    GETDIRS: Devolve os diretórios do diretório atual do servidor.
    EXIT: Finaliza a conexão.

    Autores: Caio José Cintra, Guilherme Del Rio
    Data de criação: 10/09/2022
    Data de modificação: 19/09/2022

'''

# echo-client.py
from re import I
import socket
import struct
import os

"""
                    SOLICITAÇÃO

1 byte: requisição (1) – Message Type (0x01)
1 byte: código do comando – Command Identifier (0x01 a 0x04)
1 byte: tamanho do nome do arquivo – Filename Size
variável [0-255]: nome do arquivo em bytes – Filename
     1 byte            1 byte            1 byte        [0 a 255 bytes]
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Message Type | Command Identifier | Filename Size |      Filename     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

"""


def criarCabecalho(tipoMensagem, idComando, nomeArquivo, tamanhoArquivo=None):

    bTipoMensagem = tipoMensagem.to_bytes(1, 'big')
    # print("bTipoMensagem: ", bTipoMensagem)

    bIdComando = idComando.to_bytes(1, 'big')
    # print("bIdComando: ", bIdComando)

    if(nomeArquivo != None):
        bNomeArquivo = nomeArquivo.encode("utf-8")
        # print("bNomeArquivo: ", bNomeArquivo)
    
        bTamanhoNome = len(bNomeArquivo).to_bytes(1, 'big')
        # print("bTamanhoNome: ", bTamanhoNome)

    if(idComando == 1):
        bTamanhoArquivo = tamanhoArquivo.to_bytes(4, 'big')
        # print("bTamanhoArquivo: ", bTamanhoArquivo)
        cabecalho = bTipoMensagem + bIdComando + bTamanhoNome + bNomeArquivo + bTamanhoArquivo

        print("cabecalho: ", cabecalho)
        return cabecalho

    if(idComando == 3):
        cabecalho = bTipoMensagem + bIdComando
        print("cabecalho: ", cabecalho)
        return cabecalho

    cabecalho = bTipoMensagem + bIdComando + bTamanhoNome + bNomeArquivo
    print("cabecalho: ", cabecalho)
    return cabecalho


def main():

    # IP da máquina conectada, por padrão 127.0.0.1
    ip = "127.0.0.1"

    # Porta usada para conexão
    port = 65432

    addr = (ip, port) 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.connect(addr)
    

    while True:
        comando = input("Comando: ") 

        if(comando.split()[0] == "ADDFILE"):
            nomeArquivo = comando.split()[1]
            try:
                tamanhoArquivo = os.path.getsize(nomeArquivo)
                cabecalho = criarCabecalho(1, 1, nomeArquivo, tamanhoArquivo)
            except:
                print("Arquivo não encontrado")
                continue
            

            client_socket.send(cabecalho)

            # Envia o arquivo byte a byte
            with open(nomeArquivo, 'rb') as file:
                byte = file.read(1)
                while byte != b'':
                    client_socket.send(byte)
                    byte = file.read(1)


        if(comando.split()[0] == "DELETE"):
            nomeArquivo = comando.split()[1]
            try:
                tamanhoArquivo = os.path.getsize(nomeArquivo)
                cabecalho = criarCabecalho(1, 2, nomeArquivo)
                client_socket.send(cabecalho)
            except:
                print("Arquivo não encontrado")
                continue

        if(comando.split()[0] == "GETFILESLIST"):
            cabecalho = criarCabecalho(1, 3, None)
            client_socket.send(cabecalho)

        respostaServidor = client_socket.recv(1024)
        print("Resposta do servidor: ", respostaServidor)
        

        if(respostaServidor[1:2] == b'\x03'):
            qtdArquivos = int.from_bytes(respostaServidor[3:4], 'big')
            print("qtdArquivos: ", qtdArquivos)
            arquivos = respostaServidor[4:]
            # print("arquivos split: ", arquivos)
            x = 0
            for i in range(qtdArquivos):
                tamanhoNome = int.from_bytes(arquivos[i+x:i+x+1], 'big')
                # print("tamanhoNome: ", tamanhoNome)
                nomeArquivo = arquivos[i+x+1:i+x+1+tamanhoNome].decode("utf-8")
                print("nomeArquivo: ", nomeArquivo)
                x += tamanhoNome

        messageType = int.from_bytes(respostaServidor[:1], 'big')
        # print("messageType: ", messageType)

        commandIdentifier = int.from_bytes(respostaServidor[1:2], 'big')
        # print("commandIdentifier: ", commandIdentifier)

        statusCode = int.from_bytes(respostaServidor[2:3], 'big')
        # print("statusCode: ", statusCode)

        if(statusCode == 1):
            print("Operação realizada com sucesso")
        else:
            print("Erro na operação")




        # if resposta[0] == "EXIT":
        #     break

main()