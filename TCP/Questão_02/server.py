"""
Solicitações:
----------------------------------------------------------------
|     0x01     |   0x01 a 0x04  |               | 0 a 255bytes |
----------------------------------------------------------------
| Message Type | Command Ident. | Filename Size |   Filename   |
----------------------------------------------------------------


Respostas:
------------------------------------------------------
|     0x02     |   0x01 a 0x04  | 1-SUCCESS, 2-ERROR |
------------------------------------------------------
| Message Type | Command Ident. |     Status Code    |
------------------------------------------------------
"""



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
        resposta = socket.recv(1024)

        # Decodifica a mensagem
        msg_str = resposta.decode('utf-8')
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