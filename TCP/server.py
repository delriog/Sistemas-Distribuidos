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

import threading 
import socket 
import os

host = ""
porta = 65432
addr = (host,porta) 

login_database = {"rio": "123mudar",
                  "caio": "123mudar"}

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
serv_socket.bind(addr)


def handler(ip, porta, socket):
    while True:
        # Recebe a mensagem
        msg = socket.recv(1024)

        # Decodifica a mensagem
        msg_str = msg.decode('utf-8')
        # CONNECT rio,123mudar
        msg_str = msg_str.split(' ')
        

        # Notifica servidor sobre a saída do cliente
        if msg_str[0] == 'EXIT':
            print('Cliente com o ip: ', ip, ', na porta: ', porta, ', foi desconectado!')
            resposta = "EXIT" 
            socket.send(resposta.encode('utf-8'))
            break
        
        print("mensagem:" , msg_str)

        # CONNECT
        if msg_str[0] == 'CONNECT':

            # Divide o nome de login e senha em duas string
            dados_login = msg_str[1].split(',')

            # Confere se os dados são compatíveis com os cadastrados
            if dados_login[0] in login_database and login_database[dados_login[0]] == dados_login[1]:

                # Caso o login for bem sucedido, imprime SUCCESS na tela
                resposta = "SUCCESS"
                socket.send(resposta.encode('utf-8'))
                continue

            else:

                # Caso o login não for bem sucedido, imprime ERROR na tela
                resposta = "ERROR"
                socket.send(resposta.encode('utf-8'))
                continue

        #PWD
        if msg_str[0] == 'PWD':

            # Usa a função getcwd para conseguir o endereço do diretório
            resposta = "PWD " + os.getcwd()

            # O resultado é enviado ao cliente e é impresso na tela
            socket.send(resposta.encode('utf-8'))
            print("PWD: ", resposta)
            continue
        
        # CHDIR
        if msg_str[0] == "CHDIR":
            try:

                # Executa o comando chdir para alterar o diretório para o desejado
                os.chdir(msg_str[1])

                # Caso ocorra com sucesso ele retorna SUCCESS
                resposta = "CHDIR SUCCESS"
                socket.send(resposta.encode('utf-8'))
            except:
                
                # Caso ocorra algum problema ele retorna ERROR
                resposta = "CHDIR ERROR"
                socket.send(resposta.encode('utf-8'))
            continue
        
        #GETFILES
        if msg_str[0] == 'GETFILES':

            # Usa o comando listdir para receber uma lista com os arquivos e pastas
            arquivos = os.listdir()

            # Contador de arquivos inicializado com o valor 0
            contador = 0

            # Imprime os nomes dos arquivos encontrados
            print(arquivos)

            files_list = "GETFILES " #identificador que será enviado juntamente com a string para ser tratado no client
            for nome in arquivos:
                # Verifica os arquivos com um '.' no nome (extensão) para diferenciar de um diretório
                if "." in nome:
                    # A cada arquivo encontrado, o nome dele é colocado na lista de arquivos e incrementado o contador
                    files_list += str(nome) + ","
                    contador += 1
            files_list += str(contador)
            # Após passar por todos arquivos, a lista é devolvida para o usuário
            socket.send(files_list.encode('utf-8'))
            continue

        if msg_str[0] == 'GETDIRS':
            # Usa o comando listdir para receber uma lista com os arquivos e pastas
            pastas = os.listdir()

            # Contador de pastas inicializado com o valor 0
            contador = 0

            # Imprime os nomes dos arquivos encontrados
            print("pastas: ", pastas)

            folders_list = "GETDIRS " #identificador que será enviado juntamente com a string para ser tratado no client
            for nome in pastas:
                # Verifica os arquivos sem um '.' no nome (extensão) para diferenciar de um arquivo
                if "." not in nome:
                    # A cada pasta encontrada, o nome é colocado na lista de pastas e incrementado o contador
                    folders_list += str(nome) + ","
                    contador += 1
            folders_list += str(contador)
            print("folders_list: ", folders_list)

            # Após passar por todas pastas, a lista é devolvida para o usuário
            socket.send(folders_list.encode('utf-8'))

            continue
        
        resposta = "ERROR"
        socket.send(resposta.encode('utf-8'))

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