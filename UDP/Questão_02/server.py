'''

    Programação com sockets UDP

    Descrição: Sistema de upload de arquivos via UDP

    Um servidor UDP que recebe as partes dos arquivos (1024 bytes), verifica ao final a integridade via um checksum (SHA-1) 
    e armazena o arquivo em uma pasta padrão.

    Autores: Caio José Cintra, Guilherme Del Rio
    Data de criação: 24/09/2022
    Data de modificação: 27/09/2022

'''

import socket
import math
import os
import hashlib
import logging
import logging.handlers
import datetime

# IP da máquina conectada, por padrão 127.0.0.1
localIP     = "127.0.0.1"

# Porta usada para conexão
localPort   = 6666

# Tamanho do buffer
bufferSize  = 1024

# Configuração do sistema de log
handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", "serverLog.log"))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)


def main():

	# Cria socket
	UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

	# Conecta o socket no IP e porta de destino
	UDPServerSocket.bind((localIP, localPort))
	
	print("Servidor UDP iniciado na porta: ", localPort)

	# Laço principal de execução
	while(True):

		# Recebe o cabeçalho
		msg, address = UDPServerSocket.recvfrom(bufferSize)

		# Divide os dados do cabeçalho
		tamanhoNomeArquivo = int.from_bytes(msg[0:1], 'big')
		nomeArquivo = msg[1:1+int(tamanhoNomeArquivo)].decode('utf-8')
		tamanhoArquivo = int.from_bytes(msg[1+int(tamanhoNomeArquivo):], 'big')

		# Divide o tamanho do arquivo pelo do buffer para encontrar o total de pacotes
		pacotes = tamanhoArquivo/bufferSize

		# Variável de controle
		pacote = 0

		# Cria arquivo com o nome recebido
		file2 = open('./Arquivos/' + nomeArquivo, 'wb+')
		
		# Enquanto a variável de controle for menor que a quantidade de pacotes
		while pacote < int(math.ceil(pacotes)):

			# No início da transferência, adiciona o log de registro de tempo
			if pacote == 0:
				hora = datetime.datetime.now()
				logging.info('%s: Inicio do recebimento do arquivo: %s com tamanho: %s', hora, nomeArquivo, tamanhoArquivo)

			# Recebe o pacote
			data, addr = UDPServerSocket.recvfrom(bufferSize)
			# Escreve o pacote no arquivo
			file2.write(data)
			pacote += 1

		# No Final adiciona o log de registro de tempo
		hora = datetime.datetime.now()
		logging.info('%s: Final do recebimento do arquivo: %s com tamanho: %s', hora, nomeArquivo, tamanhoArquivo)

		file2.seek(0) # Volta para o começo do arquivo

		# Obtêm o checksum do arquivo inteiro
		checksum = hashlib.sha1(file2.read()).hexdigest()
		print("checksum: ", checksum)

		# Fecha o arquivo
		file2.close()

		# Recebe o checksum do client
		checksumClient, addr = UDPServerSocket.recvfrom(bufferSize)
		print("checksumClient: ", checksumClient.decode('utf-8'))

		# Compara se os dois checksum são iguais
		if checksumClient.decode('utf-8') == checksum:
			# Caso sejam iguais retorna uma mensagem de sucesso
			hora = datetime.datetime.now()
			logging.info('%s: Arquivo recebido com sucesso: %s com tamanho: %s', hora, nomeArquivo, tamanhoArquivo)
			resposta = "Arquivo recebido com sucesso"
			UDPServerSocket.sendto(resposta.encode('utf-8'), address)

		else:

			# Caso não sejam iguais retorna uma mensagem de erro
			hora = datetime.datetime.now()
			logging.info('%s: Arquivo recebido com falha: %s com tamanho: %s', hora, nomeArquivo, tamanhoArquivo)
			resposta = "Arquivo recebido com falha"
			UDPServerSocket.sendto(resposta.encode('utf-8'), address)
			
			os.remove('./Arquivos/' + nomeArquivo) # Deleta o arquivo

main()