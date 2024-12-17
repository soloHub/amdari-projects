# Use a Python base image
FROM bitnami/python:3.10

# Set working directory
WORKDIR /app

# Copy producer.py, .env, and requirements.txt into the container
COPY producer.py /app/producer.py
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install -r requirements.txt

# Run the producer.py file when the container starts
CMD ["python", "producer.py"]