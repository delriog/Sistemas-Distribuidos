'''
    


+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|              |           |                        |              |                              |
| Message Type | Nick Size | Nick (Nick Size bytes) | Message Size | Message (Message Size bytes) |
|    1 byte    |   1 byte  |      1 a 64 bytes      |    1 byte    |         0 a 255 bytes        |
|              |           |                        |              |                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
'''

import threading
import socket
import sys
import emoji

ip = "127.0.0.1"
portas = [6666, 3333]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def cria_cabecalho(tipo_mensagem, nick, mensagem):

    tipo_mensagem = tipo_mensagem.to_bytes(1, 'big')
    nick = nick.encode('utf-8')
    tamanho_nick = len(nick).to_bytes(1, 'big')
    mensagem = mensagem.encode('utf-8')
    tamanho_mensagem = len(mensagem).to_bytes(1, 'big')
    return tipo_mensagem + tamanho_nick + nick + tamanho_mensagem + mensagem


def envia(ip, porta):
    addr = ip, porta
    divisor = "\n|------------------------------------------------------------------------------|\n"
    print(divisor, "1: mensagem normal", divisor, "2: emoji", divisor, "3: URL", divisor, "4: ECHO (envia e recebe a mesma mensagem para indicar que usuário está ativo)", divisor)

    while(True):
        msg = input('Mensagem (index:mensagem) >> ')
        try: 
            index, mensagem = msg.split(':', 1)
            if(len(mensagem) > 255):
                print('ERRO: O tamanho máximo da mensagem foi ultrapassado!')
                continue
            cabecalho = cria_cabecalho(int(index), apelido, mensagem)
        except:
            print("ERRO: Formato de mensagem inválido!")
            continue
        # print(cabecalho)
        

        sock.sendto(cabecalho, addr)
        


def recebe(ip, porta):
    addr = ip, porta
    sock.bind((ip, int(porta)))

    while(True):
        msg, addr = sock.recvfrom(1024)
        # print ("msg recebida:", msg, end=' | ')

        tipo_mensagem = int.from_bytes(msg[:1], 'big')
        # print("tipo_mensagem:", tipo_mensagem, end=' | ')

        tamanho_nick = int.from_bytes(msg[1:2], 'big')
        # print("tamanho_nick:", tamanho_nick, end=' | ')

        nick = msg[2:2+int(tamanho_nick)].decode('utf-8')
        # print("nick:", nick, end=' | ')

        tamanho_mensagem = int.from_bytes(msg[2+int(tamanho_nick):3+int(tamanho_nick)], 'big')
        # print("tamanho_mensagem:", tamanho_mensagem)

        mensagem = msg[3+int(tamanho_nick):].decode('utf-8')

        if(tipo_mensagem == 4):
            msg = cria_cabecalho(1, apelido, mensagem)
            sock.sendto(msg, addr)

        if(tipo_mensagem == 2):
            print(nick, ":", emoji.emojize(mensagem))
            continue
        
        print(nick,":", mensagem)


def main():
    
    index = sys.argv[1]
    
    global apelido

    while(True):
        apelido = input("Escreva seu apelido >> ")

        if (len(apelido.encode('utf-8')) > 255):
            print('ERRO: O tamanho máximo do apelido foi ultrapassado!')
            
        else:
            break


    try:
        if(index == "1"):
            threading.Thread(target=recebe, args=(ip, portas[1])).start()
            threading.Thread(target=envia, args=(ip, portas[0])).start()
        # Verifica se o id do cliente é 2
        elif(index == "2"):
            threading.Thread(target=recebe, args=(ip, portas[0])).start()
            threading.Thread(target=envia, args=(ip, portas[1])).start()
    except:
        print("ERRO: Erro ao criar thread!")

main()