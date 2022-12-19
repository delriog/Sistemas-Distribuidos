import tweepy
from config import *
import pika

# setting up RabbitMQ queue
connection = pika.BlockingConnection(pika.ConnectionParameters(HOST))
channel = connection.channel()


def main():

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    channel.queue_declare(queue=QUEUE)


    query = ''
    for topico in TOPICS:
        if topico == TOPICS[-1]:
            query += topico
        else:
            query += topico + " OR "

    response = client.search_recent_tweets(query=query, max_results=100)


    for tweet in response.data:
        print(tweet.text)
        channel.exchange_declare(exchange="tweets", exchange_type='direct')
        channel.basic_publish(exchange='', routing_key="tweets", body= tweet.text)
    
    connection.close()

        


if __name__ == '__main__':
    main()