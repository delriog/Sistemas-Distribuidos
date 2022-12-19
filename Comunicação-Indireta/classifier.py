import pika
import sys
from config import *

from pika import connection
from pika.spec import Channel


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()

    # Crio a lista tweet
    channel.queue_declare(queue="tweets")


    def callback(ch, method, properties, body):
            # Converto para string
            data = body.decode()

            # Verifico quais palavras pertencem ao tweet
            for topic in TOPICS:
                if topic in data.lower():
                    print("Topico: ", topic)
                    # Fila que será utilizada para troca de mensagens entre o classificador e cliente
                    channel.exchange_declare(exchange="direct_logs", exchange_type='direct')
                    # Envio para a fila de tópico correspondente ao tweet
                    channel.basic_publish(exchange="direct_logs", routing_key=str(topic), body=body)


    channel.basic_consume(queue="tweets", on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Encerrado")