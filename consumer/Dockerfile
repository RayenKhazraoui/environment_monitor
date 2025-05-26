FROM python:3.10

WORKDIR /app

# Copy both consumers
COPY consumer.py co2_consumer.py ./

# Install dependencies
RUN pip install --no-cache-dir confluent-kafka psycopg2-binary

# Launch both in parallel
CMD ["sh", "-c", "python consumer.py & python co2_consumer.py"]
