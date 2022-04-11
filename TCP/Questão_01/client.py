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
from sqlite3 import connect 

# IP da máquina conectada, por padrão 127.0.0.1
ip = "127.0.0.1"

# Porta usada para conexão
port = 65432

addr = (ip, port) 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect(addr)


def main():

    # O usuário está desconectado por padrão
    connected = False

    while True:
        comando = input("Comando: ") 
        # Envia mensagem
        client_socket.send(comando.encode("utf-8"))
        resposta = client_socket.recv(1024).decode("utf-8")
        resposta = resposta.split(' ')

        # Caso o login for bem sucedido o usuário é conectado
        if resposta[0] == 'SUCCESS' and not connected:
            print(resposta[0])
            connected = True

        #Verifica se o usuário está conectado
        if connected:

            # Se o usuário estiver conectado e receber EXIT, a conexão é fechada
            if resposta[0] == 'EXIT':
                client_socket.close()
                break
            
            #Imprime o endereço do comando PWD 
            if resposta[0] == 'PWD':
                print(resposta[1])

            #Imprime o resultado de CHDIR
            if resposta[0] == 'CHDIR':
                print(resposta[1])
            
            # Imprime os resultados do GETFILES
            if resposta[0] == 'GETFILES':
                arquivos = resposta[1].split(",")
                
                # Imprime o número de arquivos e em seguida o nome de todos eles
                print("Número de arquivos: ", arquivos[-1:])
                print("Arquivos: ")
                for arquivo in range(len(arquivos)-1):
                    print(arquivos[arquivo])
            
            # Imprime os resultados do GETDIRS
            if resposta[0] == 'GETDIRS':
                pastas = resposta[1].split(",")
                
                # Imprime o número de pastas e em seguida o nome de todas elas
                print("Número de pastas: ", pastas[-1:])
                print("Pastas: ")
                for pasta in range(len(pastas)-1):
                    print(pastas[pasta])

        else:
            # Caso qualquer comando tente ser executado sem algum usuário conectado, imprime a seguinte mensagem:
            print(resposta[0], "you are not connected")

main()