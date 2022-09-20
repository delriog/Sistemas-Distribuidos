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
import socket
import hashlib


def main():

    # IP da máquina conectada, por padrão 127.0.0.1
    ip = "127.0.0.1"

    # Porta usada para conexão
    port = 65432

    addr = (ip, port) 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.connect(addr)

    # O usuário está desconectado por padrão
    connected = False

    while True:
        comando = input("Comando: ") 
        # Envia mensagem
        if "CONNECT" in comando:
            senha = comando.split(",")[1]
            hash = hashlib.sha512( str( senha ).encode("utf-8") ).hexdigest()
            comando = comando.split(",")[0] + "," + hash

        client_socket.send(comando.encode("utf-8"))
        resposta = client_socket.recv(1024).decode("utf-8")
        print("resposta: ", resposta)

        if resposta[0] == "EXIT":
            break

main()