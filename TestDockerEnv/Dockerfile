# Use the official Ubuntu image as the base
FROM ubuntu:22.04

# Update the package lists
RUN apt-get update -y

# Install a package as an example
RUN apt-get install -y vim

# Create a directory in the container
RUN mkdir /app

# Expose a port (optional, if you want to expose a service)
# EXPOSE 8080

# Set the working directory
WORKDIR /app

# Copy a local file or directory to the container
COPY . .

# Mount a host directory to the container directory
VOLUME /app

# # 
# FROM bitnami/spark:3.5.3

# RUN apt-get update && \
#     apt-get install -y default-jre && \
#     wget https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.13/3.5.3/spark-sql-kafka-0-10_2.13-3.5.3.jar && \
#     cp spark-sql-kafka-0-10_2.12-3.5.3.jar /opt/bitnami/spark/lib/ && \
#     wget https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.12/10.4.0/mongo-spark-connector_2.12-10.4.0.jar && \
#     cp mongo-spark-connector_2.12-10.4.0.jar /opt/bitnami/spark/lib/