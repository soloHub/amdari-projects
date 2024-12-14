FROM bitnami/spark:3.5.3

# Install findspark
RUN pip install findspark

COPY spark-sql-kafka-0-10_2.13-3.5.3.jar /opt/bitnami/spark/lib/
COPY mongo-spark-connector_2.12-10.4.0.jar /opt/bitnami/spark/lib/