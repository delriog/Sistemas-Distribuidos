import socket
import math
import os
import hashlib
import logging
import logging.handlers
import datetime

localIP     = "127.0.0.1"
localPort   = 6666
bufferSize  = 1024

handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", "serverLog.log"))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)


def main():

	UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

	UDPServerSocket.bind((localIP, localPort))
	
	print("Servidor UDP iniciado na porta: ", localPort)

	while(True):

		msg, address = UDPServerSocket.recvfrom(bufferSize)

		tamanhoNomeArquivo = int.from_bytes(msg[0:1], 'big')

		nomeArquivo = msg[1:1+int(tamanhoNomeArquivo)].decode('utf-8')

		tamanhoArquivo = int.from_bytes(msg[1+int(tamanhoNomeArquivo):], 'big')

		pacotes = tamanhoArquivo/bufferSize
		pacote = 0

		file2 = open('./Arquivos/' + nomeArquivo, 'wb+')
		
		while pacote < int(math.ceil(pacotes)):
			if pacote == 0:
				hora = datetime.datetime.now()
				logging.info('%s: Inicio do recebimento do arquivo: %s com tamanho: %s', hora, nomeArquivo, tamanhoArquivo)

			data, addr = UDPServerSocket.recvfrom(bufferSize)
			file2.write(data)
			pacote += 1

		hora = datetime.datetime.now()
		logging.info('%s: Final do recebimento do arquivo: %s com tamanho: %s', hora, nomeArquivo, tamanhoArquivo)

		file2.seek(0) # Volta para o começo do arquivo
		checksum = hashlib.sha1(file2.read()).hexdigest()
		print("checksum: ", checksum)

		
		file2.close()

		checksumClient, addr = UDPServerSocket.recvfrom(bufferSize)
		print("checksumClient: ", checksumClient.decode('utf-8'))

		if checksumClient.decode('utf-8') == checksum:
			hora = datetime.datetime.now()
			logging.info('%s: Arquivo recebido com sucesso: %s com tamanho: %s', hora, nomeArquivo, tamanhoArquivo)
			resposta = "Arquivo recebido com sucesso"
			UDPServerSocket.sendto(resposta.encode('utf-8'), address)

		else:
			hora = datetime.datetime.now()
			logging.info('%s: Arquivo recebido com falha: %s com tamanho: %s', hora, nomeArquivo, tamanhoArquivo)
			resposta = "Arquivo recebido com falha"
			UDPServerSocket.sendto(resposta.encode('utf-8'), address)
			
			os.remove('./Arquivos/' + nomeArquivo) # Deleta o arquivo

main()