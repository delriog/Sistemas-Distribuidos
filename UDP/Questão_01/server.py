'''
    Programação com Sockets UDP
    Descrição: Chat Peer-To-Peer que possibilita os clientes trocarem mensagens 
    entre si com o seguinte formato:
    
        - tipo de mensagem [1 byte]
        - tamanho apelido (tam_apl) [1 byte]
        - apelido [tam_apl (1 a 64) bytes ]
        - tamanho mensagem (tam_msg) [1 byte]
        - mensagem [tam_msg bytes]

    Os tipos de mensagem são:
        1: mensagem normal
        2: emoji
        3: URL
        4: ECHO (envia e recebe a mesma mensagem para indicar que usuário está ativo).   
    
    Autores: Caio José Cintra, Guilherme Del Rio
    Data de criação: 14/04/2022
    Data de modificação: 19/04/2022
'''

import socket
import threading

clients = list()
players = list()
PORT = 4000


def handler(client, user):
    while True:
        try:
            msg = client.recv(2048).decode("utf-8")
            print(f"{user}:  {msg}")
            broadcast(msg, client)
        except:
            deleteClient(client)
            break # sai do loop
        
        
def broadcast(msg, client):
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg.encode("utf-8")) 
            except:
                deleteClient(clientItem)

def deleteClient(client):
    clients.remove(client)
    client.close()

def main():
    users = 0
    global server
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((socket.gethostname(), PORT))
        server.listen(2)

    except: 
        return print('\nNão foi possível iniciar o servidor!\n')

    while True:
        client, addr = server.accept()
        clients.append(client)
       
        print(f'{addr} conectou.{client}')
        thread = threading.Thread(target=handler, args=[client,users])
        thread.start()
        users += 1

if __name__ == '__main__':
    main()