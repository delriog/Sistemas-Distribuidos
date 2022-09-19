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

login_database = {"rio": "93f4a4e86cf842f2a03cd2eedbcd3c72325d6833fa991b895be40204be651427652c78b9cdbdef7c01f80a0acb58f791c36d49fbaa5738970e83772cea18eba1",
                  "caio": "93f4a4e86cf842f2a03cd2eedbcd3c72325d6833fa991b895be40204be651427652c78b9cdbdef7c01f80a0acb58f791c36d49fbaa5738970e83772cea18eba1"}

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
serv_socket.bind(addr)


def handler(ip, porta, socket):
    connected = False
    while True:
        resposta = ''
        # Recebe a mensagem
        msg = socket.recv(1024).decode('utf-8')
        print('Mensagem recebida: ', msg)
        # CONNECT rio,123mudar
        msg_str = msg.split(' ')

        # Verifica o login
        if connected == False:
            if msg_str[0] == 'CONNECT':
                msg_str = msg_str[1].split(',')
                if msg_str[0] in login_database:
                    if msg_str[1] == login_database[msg_str[0]]:
                        connected = True
                        print("Connected: ",connected)
                        resposta = 'SUCCESS'
                        socket.send(resposta.encode('utf-8'))
                        continue
                    else:
                        resposta = 'ERROR WRONG PASSWORD'
                        socket.send(resposta.encode('utf-8'))
                        continue
                else:
                    resposta = 'ERROR YOU ARE NOT REGISTERED'
                    socket.send(resposta.encode('utf-8'))
                    continue
        
        print("Connected: ",connected)
        if connected == True:
            if msg_str[0] == 'PWD':
                resposta = os.getcwd()
                print("resposta pwd: ", resposta)
            elif msg_str[0] == 'CHDIR':
                try:
                    os.chdir(msg_str[1])
                    resposta = 'SUCCESS'
                except:
                    resposta = 'ERROR'
            elif msg_str[0] == 'GETFILES':
                
                arquivos = os.listdir()
                contador = 0

                listaArquivos = ""
                for nome in arquivos:
                    if "." in nome:
                        listaArquivos += str(nome) + ", "
                        contador += 1
                listaArquivos += "Numero de arquivos: " + str(contador)
                resposta = listaArquivos

            elif msg_str[0] == 'GETDIRS':

                pastas = os.listdir()

                contador = 0
                folders_list = ""

                for nome in pastas:
                    if "." not in nome:
                        folders_list += str(nome) + ", "
                        contador += 1
                folders_list += "Numero de pastas: " + str(contador)

                print("folders_list: ", folders_list)
                resposta = folders_list

            elif msg_str[0] == 'EXIT':
                resposta = 'EXIT'
                print('Cliente com o ip: ', ip, ', na porta: ', porta, ', foi desconectado!')
                resposta = "EXIT" 
                socket.send(resposta.encode('utf-8'))
                socket.close()
                break
            else:
                resposta = 'ERROR'
        else:
            resposta = 'ERROR YOU ARE NOT CONNECTED'

        print("mensagem:" , msg_str)

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