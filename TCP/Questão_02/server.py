'''

    Programação com sockets TCP

    Descrição: Servidor que processa mensagens de múltiplos clientes com as seguintes operações disponíveis:

    -> ADDFILE (1): adiciona um arquivo novo.
    -> DELETE (2): remove um arquivo existente.
    -> GETFILESLIST (3): retorna uma lista com o nome dos arquivos.
    -> GETFILE (4): faz download de um arquivo

    Autores: Caio José Cintra, Guilherme Del Rio
    Data de criação: 10/09/2022
    Data de modificação: 19/09/2022, 20/09/2022

'''

import threading 
import socket 
import os

import logging
import logging.handlers

handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "serverLog.log"))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)

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
# Cria um cabeçalho como o esquematizado acima, ele recebe em seus parametros cada um de seus campos mostrados acima

    if opcao != '': #caso houver campos adicionais no cabecalho, sera adicionado ao final do mesmo
        # print("statusCode: ", statusCode, "opcao: ", opcao)
        return messageType.to_bytes(1, 'big') + commandIdentifier.to_bytes(1, 'big') + statusCode.to_bytes(1, 'big') + opcao

    return messageType.to_bytes(1, 'big') + commandIdentifier.to_bytes(1, 'big') + statusCode.to_bytes(1, 'big')

def handler(ip, porta, socket):     # Função que executa as funções do servidor, ela recebe o ip a porta e o socket para executar
    while True:
        success = False # Variavel de controle de sucesso das operações
        msg_str = socket.recv(1024)
        logging.info("mensagem recebida: %s", msg_str)

        # String de mensagem é dividida em cada informação do cabeçalho

        messageType = int.from_bytes(msg_str[:1], 'big')
        # print("messageType: ", messageType)

        commandIdentifier = int.from_bytes(msg_str[1:2], 'big')
        # print("commandIdentifier: ", commandIdentifier)

        tamanhoNome = int.from_bytes(msg_str[2:3], 'big')
        # print("tamanho nome: ", tamanhoNome)

        nomeArquivo = msg_str[3:tamanhoNome+3].decode('utf-8')
        # print('nome arquivo: ', nomeArquivo)

        listaArquivos = bytearray()
        

        if commandIdentifier == 1:      # Comando ADDFILE (1): adiciona um arquivo novo.
            print(msg_str[-4:])
            tamanhoArquivo = int.from_bytes(msg_str[-4:], 'big')
            # print("tamanhoArquivo: ", tamanhoArquivo)

            arquivo = b''
            for _ in range(tamanhoArquivo): # Recebe o arquivo byte a byte
                bytes = socket.recv(1)
                arquivo += bytes
            
            # Salva o arquivo na pasta padrão do servidor chamada 'ArquivosServer'
            with open('./ArquivosServer/' + nomeArquivo, 'w+b') as file:
                file.write(arquivo)

            logging.info("Arquivo salvo com sucesso")
            success = True # Operação bem sucedida

        elif commandIdentifier == 2:    # Comando DELETE (2): remove um arquivo existente
            try:
                os.remove('./ArquivosServer/' + nomeArquivo) # Remove o arquivo
                success = True
                logging.info("Arquivo removido com sucesso")

            except:
                pass # Caso o arquivo nao exista, pula para o envio da mensagem de erro
                logging.info("Arquivo nao encontrado")
        
        elif commandIdentifier == 3: # Comando GETFILESLIST (3): retorna uma lista com o nome dos arquivos
            arquivos = os.listdir(path='./ArquivosServer')
            # print("Arquivos: ", arquivos)

            # Identifica o número de arquivos na pasta
            qtdArquivos = len(arquivos)
            listaArquivos += qtdArquivos.to_bytes(1, 'big') # Adiciona o número de arquivos na lista de arquivos
            logging.info("qtdArquivos encontrados: %s", qtdArquivos)
            # Para cada arquivo é identificado o nome e o tamanho do nome, além de formar uma lista com os dados 
            for arquivo in arquivos:
                nome = arquivo.encode('utf-8')
                tamanhoNome = len(nome)
                # print("nome: ", nome)
                # print("tamanhoNome: ", tamanhoNome)
                # print("tamanhoNome.to_bytes(1, 'big'): ", tamanhoNome.to_bytes(1, 'big'))
                listaArquivos += tamanhoNome.to_bytes(1, 'big') + nome

            logging.info("Arquivos encontrados: %s", listaArquivos)
            success = True # Operação bem sucedida

        elif commandIdentifier == 4: # Comando GETFILE (4): retorna um arquivo
            arquivos = os.listdir(path='./ArquivosServer') # Identifica os arquivos na pasta
            # print("Arquivos: ", arquivos)

            if nomeArquivo in arquivos: # Verifica se o arquivo existe
                tamanhoArquivo = os.path.getsize('./ArquivosServer/' + nomeArquivo) # Identifica o tamanho do arquivo
                listaArquivos = b''
                listaArquivos = tamanhoArquivo.to_bytes(4, 'big') # Adiciona o tamanho do arquivo na lista de arquivos
                # print("tamanhoArquivo: ", tamanhoArquivo)
                listaArquivos += msg_str[3:tamanhoNome+3] # Adiciona o nome do arquivo na lista de arquivos
                success = True # Operação bem sucedida
                logging.info("Arquivo encontrado com sucesso: %s", nomeArquivo)
            else:
                success = False # Operação mal sucedida

        if success:
        # Em caso de sucesso cria o cabeçalho com SUCCESS
            resposta = criaCabecalho(2, commandIdentifier, 1, listaArquivos)
            logging.info("cabecalho criado com sucesso: %s", resposta)
        else:
        # Caso contrário cria o cabeçalho com ERROR
            resposta = criaCabecalho(2, commandIdentifier, 2, listaArquivos)
            logging.info("cabecalho criado com sucesso, porém operacao com erro: %s", resposta)

        # print("Resposta: ", resposta)
        socket.send(resposta)

        if commandIdentifier == 4 and success: # Caso o comando seja GETFILE e o arquivo tenha sido encontrado
            with open('./ArquivosServer/' + nomeArquivo, 'rb') as file: # Abre o arquivo
                byte = file.read(1)
                while byte != b'': # Envia o arquivo byte a byte para a pasta do cliente ArquivosClient
                    socket.send(byte)
                    byte = file.read(1)
            logging.info("Arquivo enviado com sucesso")
def main():
    vetorThreads = []
    logging.basicConfig(filename='example.log', filemode='a', level=logging.INFO)
    while True:
        # Limite de 20 conexões
        serv_socket.listen(20)

        # Servidor escuta as conexões
        (socket , (ip,porta) ) = serv_socket.accept()
        print('Cliente: ', ip, 'conectado na porta: ', porta)
        logging.info('Cliente: %s conectado na porta %s', ip, porta)

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