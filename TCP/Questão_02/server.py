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
    Data de criação: 04/04/2022
    Data de modificação: 05/04/2022

'''

from sqlite3 import connect
import threading 
import socket 
import os

host = ""
porta = 65432
addr = (host,porta) 

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
serv_socket.bind(addr)

"""
                    RESPOSTAS
1 byte: resposta (2) – Message Type (0x02)
1 byte: código do comando – Command Identifier (0x01 a 0x04)
1 byte: status code (1-SUCCESS, 2-ERROR) – Status Code
     1 byte            1 byte           1 byte    
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Message Type | Command Identifier | status code |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
"""


def handler(ip, porta, socket):
    while True:
        msg_str = socket.recv(1024)



        # socket.send(resposta.encode('utf-8'))

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
        
    # Aguarda todas as threads serem finalizadas
    for t in vetorThreads: 
        t.join()

    # Fecha conexão
    serv_socket.close()

main()