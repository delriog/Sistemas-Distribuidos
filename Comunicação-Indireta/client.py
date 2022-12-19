import pika
import sys
from config import * 

def main():

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declaro a fila para troca
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    topicos = sys.argv[1:]

    for i in range(len(topicos)):
        if topicos[i] not in TOPICS:
            sys.stderr.write("Necessario se cadastrar em um dos topicos disponiveis: \n", topicos)
            sys.exit(1)

    for topico in topicos:
        channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=topico)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    # Printo o retorn
    def callback(ch, method, properties, body):
        data = body.decode()
        print("%r" % (method.routing_key))
        print(data)
        print("------------------------------------------------------")


    # Consumindo a lista
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Encerrado")