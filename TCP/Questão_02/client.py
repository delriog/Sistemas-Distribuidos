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

# echo-client.py
from re import I
import socket
import os

"""
                    SOLICITAÇÃO

1 byte: requisição (1) – Message Type (0x01)
1 byte: código do comando – Command Identifier (0x01 a 0x04)
1 byte: tamanho do nome do arquivo – Filename Size
variável [0-255]: nome do arquivo em bytes – Filename
     1 byte            1 byte            1 byte        [0 a 255 bytes]
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Message Type | Command Identifier | Filename Size |      Filename     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

"""


def criarCabecalho(tipoMensagem, idComando, nomeArquivo, tamanhoArquivo=None): # Cria um cabeçalho como o esquematizado acima, ele recebe em seus parametros cada um de seus campos como mostrado acima

    bTipoMensagem = tipoMensagem.to_bytes(1, 'big')
    # print("bTipoMensagem: ", bTipoMensagem)

    bIdComando = idComando.to_bytes(1, 'big')
    # print("bIdComando: ", bIdComando)

    if(nomeArquivo != None): #caso houver campos adicionais no cabecalho, sera adicionado ao final do mesmo
        bNomeArquivo = nomeArquivo.encode("utf-8")
        # print("bNomeArquivo: ", bNomeArquivo)
    
        bTamanhoNome = len(bNomeArquivo).to_bytes(1, 'big')
        # print("bTamanhoNome: ", bTamanhoNome)

    if(idComando == 1): #caso o comando seja ADDFILE, o tamanho do arquivo sera adicionado ao final do cabecalho
        bTamanhoArquivo = tamanhoArquivo.to_bytes(4, 'big')
        # print("bTamanhoArquivo: ", bTamanhoArquivo)
        cabecalho = bTipoMensagem + bIdComando + bTamanhoNome + bNomeArquivo + bTamanhoArquivo

        # print("cabecalho: ", cabecalho)
        return cabecalho

    if(idComando == 3): #caso o comando seja GETFILESLIST, o tamanho do arquivo sera adicionado ao final do cabecalho
        cabecalho = bTipoMensagem + bIdComando
        # print("cabecalho: ", cabecalho)
        return cabecalho

    cabecalho = bTipoMensagem + bIdComando + bTamanhoNome + bNomeArquivo #caso o comando seja DELETE ou GETFILE, o tamanho do arquivo nao sera adicionado ao final do cabecalho
    # print("cabecalho: ", cabecalho)
    return cabecalho


def main():
    
    # IP da máquina conectada, por padrão 127.0.0.1
    ip = "127.0.0.1"

    # Porta usada para conexão
    port = 65432

    addr = (ip, port) 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.connect(addr)
    

    while True:
        comando = input("Comando: ")  # Recebe o comando do usuário

        if(comando.split()[0] == "ADDFILE"): # Caso o comando seja ADDFILE, o cabecalho sera enviado ao servidor
            nomeArquivo = comando.split()[1] 
            try:
                tamanhoArquivo = os.path.getsize(nomeArquivo) # Tamanho do arquivo
                cabecalho = criarCabecalho(1, 1, nomeArquivo, tamanhoArquivo)  # Cria o cabeçalho
            except:
                print("Arquivo não encontrado") # Caso o arquivo nao seja encontrado, sera exibida uma mensagem de erro
                continue
            

            client_socket.send(cabecalho) # Envia o cabeçalho ao servidor

            # Envia o arquivo byte a byte
            with open(nomeArquivo, 'rb') as file:
                byte = file.read(1)
                while byte != b'':
                    client_socket.send(byte)
                    byte = file.read(1)


        elif(comando.split()[0] == "DELETE"): # Caso o comando seja DELETE, o cabecalho sera enviado ao servidor com o arquivo a ser deletado
            nomeArquivo = comando.split()[1]
            try:
                tamanhoArquivo = os.path.getsize(nomeArquivo) # Tamanho do arquivo
                cabecalho = criarCabecalho(1, 2, nomeArquivo) # Cria o cabeçalho
                client_socket.send(cabecalho) # Envia o cabeçalho ao servidor
            except:
                print("Arquivo não encontrado") # Caso o arquivo nao seja encontrado, sera exibida uma mensagem de erro
                continue

        elif(comando.split()[0] == "GETFILESLIST"): # Caso o comando seja GETFILESLIST, o cabecalho sera enviado ao servidor
            cabecalho = criarCabecalho(1, 3, None) # Cria o cabeçalho
            client_socket.send(cabecalho) # Envia o cabeçalho ao servidor

        elif(comando.split()[0] == "GETFILE"): # Caso o comando seja GETFILE, o cabecalho sera enviado ao servidor com o arquivo a ser baixado
            cabecalho = criarCabecalho(1, 4, comando.split()[1]) # Cria o cabeçalho
            # print("cabecalho client: ", cabecalho)
            client_socket.send(cabecalho) # Envia o cabeçalho ao servidor

        else:
            print("Comando inválido") # Caso o comando nao seja reconhecido, sera exibida uma mensagem de erro
            continue

        respostaServidor = client_socket.recv(1024) # Recebe a resposta do servidor
        # print("Resposta do servidor: ", respostaServidor)
        

        if(respostaServidor[1:2] == b'\x03'): # Caso o comando seja GETFILESLIST, o servidor ira retornar uma lista de arquivos
            qtdArquivos = int.from_bytes(respostaServidor[3:4], 'big') # Quantidade de arquivos
            print("Quantidade de arquivos: ", qtdArquivos) # Exibe a quantidade de arquivos
            arquivos = respostaServidor[4:] # Lista de arquivos
            # print("arquivos split: ", arquivos)
            x = 0 # Variavel auxiliar
            for i in range(qtdArquivos): # Exibe a lista de arquivos
                tamanhoNome = int.from_bytes(arquivos[i+x:i+x+1], 'big') # Tamanho do nome do arquivo
                # print("tamanhoNome: ", tamanhoNome)
                nomeArquivo = arquivos[i+x+1:i+x+1+tamanhoNome].decode("utf-8") # Nome do arquivo
                print("Nome arquivo: ", nomeArquivo) # Exibe o nome do arquivo
                x += tamanhoNome # Incrementa a variavel auxiliar

        if(respostaServidor[1:2] == b'\x04' and respostaServidor[2:3] == b'\x01'): # Caso o comando seja GETFILE e o arquivo exista, o servidor ira retornar o arquivo
            tamanhoArquivo = int.from_bytes(respostaServidor[3:7], 'big') # Tamanho do arquivo
            # print("tamanhoArquivo: ", tamanhoArquivo)
            nomeArquivo = respostaServidor[7:].decode("utf-8") # Nome do arquivo
            # print("nomeArquivo: ", nomeArquivo)
            arquivo = b'' 
            for _ in range(tamanhoArquivo): # Recebe o arquivo byte a byte
                bytes = client_socket.recv(1)
                arquivo += bytes
            
            with open('./ArquivosClient/' + nomeArquivo, 'w+b') as file: # Cria o arquivo na pasta de arquivos do cliente 
                file.write(arquivo)
        


        messageType = int.from_bytes(respostaServidor[:1], 'big') # Tipo de mensagem
        # print("messageType: ", messageType)

        commandIdentifier = int.from_bytes(respostaServidor[1:2], 'big') # Identificador do comando
        # print("commandIdentifier: ", commandIdentifier)

        statusCode = int.from_bytes(respostaServidor[2:3], 'big') # Codigo de status
        # print("statusCode: ", statusCode)

        if(statusCode == 1): # Caso o codigo de status seja 1, o comando foi executado com sucesso
            print("Operação realizada com sucesso")
        else:
            print("Erro na operação") # Caso o codigo de status seja 2, o comando nao foi executado com sucesso

main()