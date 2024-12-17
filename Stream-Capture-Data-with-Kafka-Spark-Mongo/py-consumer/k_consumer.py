from kafka import KafkaConsumer

def count_messages(topic_name, bootstrap_servers):
    consumer = KafkaConsumer(topic_name, bootstrap_servers=bootstrap_servers)
    message_count = 0
    for message in consumer:
        message_count += 1
    return message_count

# Replace with your Kafka broker address and topic name
topic_name = "reddit"
bootstrap_servers = "localhost:9092"

total_count = count_messages(topic_name, bootstrap_servers)
print(f"Total messages in {topic_name}: {total_count}")