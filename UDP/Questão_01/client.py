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

import threading
import socket

PORT = 4000

def handler(apelido):
    while True:
        separador = " "
        separador = separador.encode("utf-8")
        apelido = str(apelido)
        msg = input("~ ")
        tam_msg = len(msg.encode("utf-8"))
        tam_apl = len(apelido.encode("utf-8"))
        # Caso a mensagem possua um emoji
        if "U000" in msg:
            tipo_msg = 2
        # Caso a mensagem possua um URL
        elif "http" in msg:
            tipo_msg = 3
        # Caso a mensagem possua um echo
        elif "echo" in msg:
            tipo_msg = 4
        # Caso a mensagem não se encaixe em nenhum anterior ela é tida como mensagem normal
        else:
            tipo_msg = 1
        # Formação do cabeçalho a ser enviado
        pacote = tipo_msg.to_bytes(1, byteorder="big")+ separador + tam_apl.to_bytes(1, byteorder="big") + separador + apelido.encode("utf-8") + separador + tam_msg.to_bytes(1, byteorder="big") + separador + msg.encode("utf-8")
        print(pacote)
        s.send(pacote)

# Recebe mensagens de outros usuários
def receiver(apelido):
    while True:
        msg = s.recv(2048)
        print(msg)
        msg = msg.split()
        tipo_msg = int.from_bytes(msg[0], "big")
        tam_apl = int.from_bytes(msg[1], "big")
        apelido = msg[2].decode('utf-8')
        tam_msg = int.from_bytes(msg[3], "big")
        msg = msg[4].decode('utf-8')
        print(f"{apelido}: {msg}")

def main():
    
    global s

    # Conexão com socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((socket.gethostname(), PORT))
    except:
        # Em caso de falha, é retornado erro
        return print('\nNão foi possívvel se conectar ao servidor!\n')

    # Receber o apelido do usuá
    client = input('Qual o seu apelido? ')
    send = threading.Thread(target=handler, args=[client])
    send.start()
    receive = threading.Thread(target=receiver, args=[client])
    receive.start()

if __name__ == '__main__':
    main()