'''
    Programação com Sockets UDP

    Descrição: chat P2P que possibilita os clientes trocarem mensagens entre si. 

    Formato das mesagens:

    - tipo de mensagem [1 byte]
    - tamanho apelido (tam_apl) [1 byte]
    - apelido [tam_apl (1 a 64) bytes ]
    - tamanho mensagem (tam_msg) [1 byte]
    - mensagem [tam_msg bytes]

    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |              |           |                        |              |                              |
    | Message Type | Nick Size | Nick (Nick Size bytes) | Message Size | Message (Message Size bytes) |
    |    1 byte    |   1 byte  |      1 a 64 bytes      |    1 byte    |         0 a 255 bytes        |
    |              |           |                        |              |                              |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    Os tipos de mensagem são:
    1: mensagem normal
    2: emoji
    3: URL
    4: ECHO (envia e recebe a mesma mensagem para indicar que usuário está ativo).

    Autores: Caio José Cintra, Guilherme Del Rio
    Data de criação: 24/09/2022
    Data de modificação: 27/09/2022

'''

import threading
import socket
import sys
import emoji

# IP da máquina conectada, por padrão 127.0.0.1
ip = "127.0.0.1"

# Portas usadas para conexão
portas = [6666, 3333]

# Criação de socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def cria_cabecalho(tipo_mensagem, nick, mensagem): # Função que cria o cabeçalho, ela recebe o timpo da mensagem, o nome do usuário e a mensagem enviada

    # Converte o tipo da mensagem
    tipo_mensagem = tipo_mensagem.to_bytes(1, 'big')

    # Converte o nome do usuário e obtem o tamanho 
    nick = nick.encode('utf-8')
    tamanho_nick = len(nick).to_bytes(1, 'big')

    # Converte a mensagem e obtem o tamanho
    mensagem = mensagem.encode('utf-8')
    tamanho_mensagem = len(mensagem).to_bytes(1, 'big')

    # Retorna o cabeçalho preenchido
    return tipo_mensagem + tamanho_nick + nick + tamanho_mensagem + mensagem


def envia(ip, porta): # Função para enviar mensagens, recebe o ip e a porta destino

    addr = ip, porta

    # Imprime uma tabela com os números de cada tipo de mensagem
    divisor = "\n|------------------------------------------------------------------------------|\n"
    print(divisor, "1: mensagem normal", divisor, "2: emoji", divisor, "3: URL", divisor, "4: ECHO (envia e recebe a mesma mensagem para indicar que usuário está ativo)", divisor)

    # Laço onde pede para o usuário digitar a mensagem
    while(True):
        msg = input('Mensagem (index:mensagem) >> ')
        try: 
            # A mensagem deve ter a divisão 'tipo:mensagem'
            index, mensagem = msg.split(':', 1)
            
            # Mensagem muito longa (Acima de 255 caracteres)
            if(len(mensagem) > 255):
                print('ERRO: O tamanho máximo da mensagem foi ultrapassado!')
                continue
            
            # Caso tudo ocorra certo o cabeçalho é criado
            cabecalho = cria_cabecalho(int(index), apelido, mensagem)
        except:
            # Caso contrário, uma mensagem de erro é exibida
            print("ERRO: Formato de mensagem inválido!")
            continue
        
        # Envia o cabeçalho gerado para o endereço obtido
        sock.sendto(cabecalho, addr)
        


def recebe(ip, porta):  # Função para receber a mensagem enviada, recebe por parâmetro o ip e a porta
    addr = ip, porta
    sock.bind((ip, int(porta)))

    # Laço onde o usuário continuará pordendo receber mensagens
    while(True):
        msg, addr = sock.recvfrom(1024)
        # print ("msg recebida:", msg, end=' | ')

        # Obtêm os dados do cabeçalho recebido
        tipo_mensagem = int.from_bytes(msg[:1], 'big')
        # print("tipo_mensagem:", tipo_mensagem, end=' | ')

        tamanho_nick = int.from_bytes(msg[1:2], 'big')
        # print("tamanho_nick:", tamanho_nick, end=' | ')

        nick = msg[2:2+int(tamanho_nick)].decode('utf-8')
        # print("nick:", nick, end=' | ')

        tamanho_mensagem = int.from_bytes(msg[2+int(tamanho_nick):3+int(tamanho_nick)], 'big')
        # print("tamanho_mensagem:", tamanho_mensagem)

        # Forma uma mensagem para o usuário poder visualizar
        mensagem = msg[3+int(tamanho_nick):].decode('utf-8')

        # Mensagem tipo ECHO retorna o usuário para quem enviou
        if(tipo_mensagem == 4):
            msg = cria_cabecalho(1, apelido, mensagem)
            sock.sendto(msg, addr)

        # Mensagem tipo emoji converte usando a função emojize para que o emoji apareça da forma correta
        if(tipo_mensagem == 2):
            print(nick, ":", emoji.emojize(mensagem))
            continue
        
        # Imprime a mensagem formatada
        print(nick,":", mensagem)


def main():
    
    index = sys.argv[1]
    
    global apelido

    # Laço pedindo um nome de usuário até ele ser válido
    while(True):
        apelido = input("Escreva seu apelido >> ")
        
        # Nome muito grande
        if (len(apelido.encode('utf-8')) > 255):
            print('ERRO: O tamanho máximo do apelido foi ultrapassado!')

        # Sai do laço caso nome válido   
        else:
            break


    try:
        # Cria threads para ambos os usuários
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