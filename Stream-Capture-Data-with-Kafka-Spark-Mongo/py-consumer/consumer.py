import findspark 
findspark.init()
from pyspark.sql import SparkSession

mongodb_username = "kafkadb"
mongodb_password = "password"
database = "redditdb"
collection = "politics"
uri = f'mongodb+srv://{mongodb_username}:{mongodb_password}@host.docker.internal:27017/'
brokers = "kafka:9092"
topic = "reddit"


spark = SparkSession.builder \
        .appName("RedditKafkaToMongo") \
        .config("spark.sql.sources.enabledProtocols", "kafka") \
        .config("spark.mongodb.output.uri", uri) \
        .config("spark.mongodb.output.database", database) \
        .config("spark.mongodb.output.collection", collection)\
        .getOrCreate()

kafka_stream_df = spark.readStream \
                    .format("kafka") \
                    .option("kafka.bootstrap.servers", brokers) \
                    .option("subscribe", topic) \
                    .load()

kafka_stream_df.printSchema()

kafka_stream_df = kafka_stream_df.selectExpr("CAST(value AS STRING) as data" "timestamp")
kafka_stream_df.printSchema()

kafka_stream_df \
    .writeStream \
    .outputMode("append") \
    .foreachBatch(lambda df, epoch_id: df_write.format("mongo").mode("append").save()) \
    .start() \
    .awaitTermination()