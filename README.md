# Environment monitor

Self-hosted indoor air quality monitoring system, deployed on a repurposed Linux laptop. It uses Python, Kafka, PostgreSQL, and Grafana to collect and visualize environmental sensor data from a Raspberry Pi.

## Tech Stack

- **Python** – sensor reading (producer) and data ingestion (consumer)
- **Kafka** – message broker for streaming sensor data
- **PostgreSQL** – time-series data storage
- **Grafana** – data visualization
- **Docker Compose** – container orchestration
- **Raspberry Pi** – hardware platform running the sensors
- **Linux laptop** – repurposed as a local server for hosting the database and consumers

## System Overview

- A Raspberry Pi runs a Python producer script that reads sensor data from:
  - An MH-Z19B sensor (CO2 concentration)
  - A BME280 sensor (temperature, humidity, and pressure)
- Readings from both sensors are published to a single Kafka topic
- A Python consumer running in Docker ingests the Kafka stream and writes structured sensor data to a PostgreSQL database
- Grafana, also running in Docker, visualizes the data in real time
- All backend services (Kafka, Zookeeper, PostgreSQL, Grafana, and the Kafka consumer) are hosted on a Linux laptop running headless as a local server

## Grafana Dashboard

Example visualization of real-time sensor data from PostgreSQL:

![Grafana dashboard](image/grafana.png)
