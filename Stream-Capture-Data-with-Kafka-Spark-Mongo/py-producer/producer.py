import praw
from kafka import KafkaProducer
import json
import os

client_id = 'qY-RWOFGa5YAZDQ6I_NEoA'
client_secret = 'Cqrsmn6YXnhWfcQZa3AYMR1djSqDHQ'
redirect_uri = 'http://localhost'
user_agent = 'reddit-producer'


reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    user_agent=user_agent,
)

brokers = "kafka:9092"

producer = KafkaProducer(
    bootstrap_servers=brokers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


# subreddit = reddit.subreddit("politics")

# for comment in subreddit.stream.comments():
#     producer.send("reddit", value={'comment': comment.body})
#     print("=="*40)
#     print(comment.body)

try:
    subreddit = reddit.subreddit("politics")
    for comment in subreddit.stream.comments():
        producer.send("reddit", value={'comment': comment.body})
        print("=="*40)
        print(comment.body)
except Exception as e:
    print(f"Error: {e}")