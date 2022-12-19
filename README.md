# Instalação
 
 Para execução desse projeto é necessário a instalação do RabbitMQ (https://www.rabbitmq.com/download.html)
 
 ## Exemplo de execução
 
 1- Para execução primeiramente inicie o cliente especificando os tópicos a se inscrever:
 $ python client.py topico
 
 2- Executar o classificador:
 $ python classifier.py

 3- Executar o coletor:
 $ python colector.py

Após a execução dos arquivos, o cliente exibirá dentre os 100 tweets coletados, os que contém palavras com seu tópico.
