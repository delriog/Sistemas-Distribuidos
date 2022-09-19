'''

    Programação com sockets TCP

    Descrição: Servidor que processa mensagens de múltiplos clientes com as seguintes operações disponíveis:

    CONNECT user,password: Conecta o usuário na servidor usando sua senha, em caso de sucesso deveolvendo SUCCESS e caso contrário devolvendo ERROR,
    enquanto o usuário não está conectado ele não pode executar comandos.
    PWD: Devolve o caminho corrente usando String UTF, separando diretórios por barra.
    CHDIR path: Altera o diretório atual para path, retornando SUCCESS caso seja bem sucedido e ERROR caso contrário.
    GETFILES: Devolve os arquivos do diretório atual no servidor.
    GETDIRS: Devolve os diretórios do diretório atual do servidor.
    EXIT: Finaliza a conexão.
    
    Autores: Caio José Cintra, Guilherme Del Rio
    Data de criação: 04/04/2022
    Data de modificação: 05/04/2022

'''

# echo-client.py
import socket
import struct


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


def criarCabecalho(tipoMensagem, idComando, tamanhoNome, nomeArquivo):
    cabecalho = bytearray(3)
    bNomeArquivo = bytearray(nomeArquivo, 'utf-8')
    cabecalho[0] = tipoMensagem
    cabecalho[1] = idComando
    cabecalho[2] = tamanhoNome
    
    print("Byte: ", cabecalho, "nome arquivo: ", bNomeArquivo)

    return cabecalho, bNomeArquivo


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
        resposta = input("Comando: ") 

        print("resposta: ", resposta)
        if(resposta.split()[0] == "ADDFILE"):
            nomeArquivo = resposta.split()[1]
            cabecalho, bnomeArquivo = criarCabecalho(1, 1, len(nomeArquivo), nomeArquivo)


        client_socket.send(cabecalho + bnomeArquivo)
        # resposta = client_socket.recv(1024).decode("utf-8")





        # if resposta[0] == "EXIT":
        #     break

main()