from kafka import KafkaProducer

try:
    # Kafka broker on Docker
    brokers = "localhost:9092"

    # Initialize producer
    producer = KafkaProducer(
        bootstrap_servers=brokers,
        value_serializer=lambda v: v.encode('utf-8'),  # Serialize message as UTF-8
        acks='all'  # Ensure producer waits for confirmation
    )

    # Send message to a topic
    topic = "test"
    producer.send(topic, value="Hello from host!")

    # Flush to ensure message is sent
    producer.flush()
    print(f"Message sent to {topic}!")

    # Close producer
    producer.close()

except Exception as e:
    print(f"Error: {e}")

# try:
#     producer = KafkaProducer(bootstrap_servers='localhost:9092')
#     producer.send('test', b'Test message')
#     producer.close()
# except Exception as e:
#     print(f"Error: {e}")
