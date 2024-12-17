# Stage 1: Build stage to install dependencies
FROM python:3.10-slim AS build-stage

# Set working directory
WORKDIR /app

# Copy application files
COPY consumer.py ./consumer.py
COPY requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install -r requirements.txt

# Stage 2: Final lightweight runtime image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy application files and dependencies from the build stage
COPY --from=build-stage /app /app

# (Optional) Install Java if required
RUN apt-get update && apt-get install -y openjdk-21-jdk-headless && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable if Java is installed
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Command to run the application
CMD ["python", "consumer.py"]



# Use a multi-stage build for efficiency
# FROM eclipse-temurin:21 AS build-stage

# # Copy consumer.py and requirements.txt into the build stage
# COPY consumer.py ./consumer.py
# COPY requirements.txt ./requirements.txt

# # Install Python dependencies in the build stage
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the application code and dependencies to the final image
# FROM bitnami/python:3.10

# # Set working directory
# WORKDIR /app

# # Copy the application files from the build stage
# COPY --from=build-stage $JAVA_HOME $JAVA_HOME

# # Set JAVA_HOME environment variable
# ENV JAVA_HOME=/opt/java/openjdk

# ENV PATH="${JAVA_HOME}/bin:${PATH}"

# # Expose a port (optional, if your consumer.py needs to listen on a port)
# # EXPOSE 8080

# # Command to run when the container starts
# CMD ["python", "consumer.py"]

# # Use a Python base image to simplify the setup
# FROM bitnami/python:3.10 AS base-stage

# # Set working directory
# WORKDIR /app

# # Copy application files
# COPY consumer.py ./consumer.py
# COPY requirements.txt ./requirements.txt

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Use a runtime-specific base image for a smaller final image
# # FROM bitnami/python:3.10

# # Set working directory
# WORKDIR /app

# # Copy dependencies and application files from the build stage
# # COPY --from=base-stage /app /app

# # (Optional) If Java is actually required, install it here
# RUN apt-get update && apt-get install -y openjdk-21-jdk && rm -rf /var/lib/apt/lists/*

# # Set JAVA_HOME environment variable
# ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
# ENV PATH="${JAVA_HOME}/bin:${PATH}"

# # Expose a port (optional, if your application listens on a port)
# # EXPOSE 8080

# # Command to run the application
# CMD ["python", "consumer.py"]
