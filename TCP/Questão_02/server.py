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

def criaCabecalho(messageType, commandIdentifier, statusCode, opcao):
    if statusCode:
        statusCode = 1
    else:
        statusCode = 2

    if opcao != '':
        return messageType.to_bytes(1, 'big') + commandIdentifier.to_bytes(1, 'big') + statusCode.to_bytes(1, 'big') + opcao

    return messageType.to_bytes(1, 'big') + commandIdentifier.to_bytes(1, 'big') + statusCode.to_bytes(1, 'big')

def handler(ip, porta, socket):
    while True:
        success = False
        msg_str = socket.recv(1024)

        messageType = int.from_bytes(msg_str[:1], 'big')
        print("messageType: ", messageType)

        commandIdentifier = int.from_bytes(msg_str[1:2], 'big')
        print("commandIdentifier: ", commandIdentifier)

        tamanhoNome = int.from_bytes(msg_str[2:3], 'big')
        print("tamanhoNome: ", tamanhoNome)

        nomeArquivo = msg_str[3:tamanhoNome+3].decode('utf-8')
        print('Mensagem recebida: ', nomeArquivo)

        listaArquivos = bytearray()
        

        if commandIdentifier == 1:
            print(msg_str[-4:])
            tamanhoArquivo = int.from_bytes(msg_str[-4:], 'big')
            print("tamanhoArquivo: ", tamanhoArquivo)

            arquivo = b''
            for _ in range(tamanhoArquivo):
                bytes = socket.recv(1)
                arquivo += bytes
            
            # Salva o arquivo
            with open('./Arquivos/' + nomeArquivo, 'w+b') as file:
                file.write(arquivo)

            success = True

        elif commandIdentifier == 2:
            try:
                os.remove('./Arquivos/' + nomeArquivo)
                success = True
            except:
                pass
        
        elif commandIdentifier == 3:
            arquivos = os.listdir(path='./Arquivos')
            print("Arquivos: ", arquivos)

            qtdArquivos = len(arquivos)
            listaArquivos += qtdArquivos.to_bytes(1, 'big')
            for arquivo in arquivos:
                nome = arquivo.encode('utf-8')
                tamanhoNome = len(nome)
                print("nome: ", nome)
                print("tamanhoNome: ", tamanhoNome)
                print("tamanhoNome.to_bytes(1, 'big'): ", tamanhoNome.to_bytes(1, 'big'))
                listaArquivos += tamanhoNome.to_bytes(1, 'big') + nome
            
            success = True


        if success:
            resposta = criaCabecalho(2, commandIdentifier, 1, listaArquivos)
        else:
            resposta = criaCabecalho(2, commandIdentifier, 2, listaArquivos)

        print("Resposta: ", resposta)
        socket.send(resposta)

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