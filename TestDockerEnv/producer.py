import praw
from kafka import KafkaProducer
import json
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

client_id = os.getenv("ID")
client_secret = os.getenv("SECRET")
redirect_uri = 'http://localhost'
user_agent = 'reddit-producer'


reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    user_agent=user_agent,
)

brokers = "0.0.0.0:9092"

producer = KafkaProducer(
    bootstrap_servers=brokers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


subreddit = reddit.subreddit("politics")

for comment in subreddit.stream.comments():
    producer.send("reddit", value={'comment': comment.body})