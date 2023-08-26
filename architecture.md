# Project Architecture

This document provides an overview of the software architecture of the MQTT data acquisition and transformation project. The architecture is designed to handle data acquisition from various devices through MQTT, perform data transformation, and output the transformed data to the screen. Additionally, monitoring and alerting mechanisms are integrated to ensure the reliability and performance of the system.

## Overview

The project's architecture is built to process data from energy equipment such as PV inverters or batteries through MQTT messages. The data is acquired and transformed before being presented on the screen. The architecture incorporates several components to achieve these goals.

## Project Structure

```
├── Dockerfile             # Docker configuration for containerization
├── README.md              # Project documentation
├── architecture.md        # Detailed explanation of the software architecture
├── ca-stage.crt           # TLS/SSL certificate file
├── config_logging.py      # Logging configuration module
├── main.py                # Entry point of the application
├── mqtt_client.py         # MQTT client implementation
├── requirements.txt       # Required Python packages
├── transform.py           # Data transformation module
├── test                   # Unit tests directory
│   ├── __init__.py
│   ├── __pycache__
│   └── test_transform.py
├── monitoring             # Monitoring configuration
│   └── prometheus.yml     # Prometheus configuration for metrics monitoring
├── data                   # Example directory for storing data files from monitoring
│   ├── chunks_head
│   ├── queries.active
│   └── wal
└── venv                   # Virtual environment directory
    ├── bin
    ├── lib
    └── pyvenv.cfg
```

## Directory Structure

1. **Dockerfile**: Configuration file for building the Docker container.

2. **README.md**: Project documentation with information about setup, usage, and deployment.

3. **architecture.md**: A detailed explanation of the software architecture, workflow, and components.

4. **ca-stage.crt**: TLS/SSL certificate file for secure MQTT communication.

5. **config_logging.py**: Module to configure the logging system.

6. **main.py**: Entry point of the application that connects to the MQTT broker, processes messages, and displays transformed data.

7. **mqtt_client.py**: MQTT client implementation for connecting to the MQTT broker and handling messages.

8. **requirements.txt**: List of required Python packages for the project.

9. **transform.py**: Module for transforming MQTT payload data into structured format.

10. **test**: Directory containing unit tests for the project.

11. **monitoring**: Configuration directory for monitoring tools.

    - **prometheus.yml**: Prometheus configuration file for collecting and monitoring metrics.

12. **venv**: Virtual environment directory for isolating Python dependencies.

The project structure follows a modular approach, separating different components and functionalities for better organization, maintainability, and testability.

## Components

### MQTT Data Acquisition

1. **Dataloggers**: These are deployed at various sites to read data directly from energy equipment. They send the acquired data over MQTT to the main AMMP MQTT broker at `mqtt.ammp.io`.

2. **MQTT Broker**: The main MQTT broker (`mqtt.ammp.io`) receives MQTT messages from dataloggers and facilitates their distribution to subscribers.

### MQTT Client

1. **Client**: The MQTT client connects to the MQTT broker to subscribe to a specific topic where data messages are published. The client is responsible for processing incoming MQTT messages.

2. **Message Transformation**: Upon receiving a message, the MQTT client invokes the `transform_payload` function to transform the data from JSON format to a structured data pipeline format.

### Data Transformation

1. **transform_payload**: This module performs data transformation by parsing the JSON payload and extracting relevant information. The transformed data is structured and ready for display.

### Monitoring and Alerts

1. **Basic Metrics**: The MQTT client incorporates basic monitoring by tracking the number of messages processed. This metric provides insight into the message processing rate.

2. **Alerts via Email**: The MQTT client is equipped to send email alerts when certain thresholds are met. For example, an alert can be triggered if the number of processed messages exceeds a predetermined limit.

## Workflow

1. Dataloggers collect data from energy equipment and send MQTT messages to the main AMMP MQTT broker.

2. The MQTT client subscribes to a specific topic on the broker to receive incoming messages.

3. Upon receiving an MQTT message, the client invokes the `transform_payload` function to convert the JSON payload into a structured data format.

4. Transformed data is displayed on the screen, providing users with a clear view of the acquired and processed data.

5. Basic metrics are tracked to monitor the processing rate of messages.

6. If a predefined threshold is reached, an email alert is sent to notify stakeholders of the threshold breach.

## Conclusion

The architecture of the MQTT data acquisition and transformation project efficiently handles data collection, transformation, and display. By incorporating basic monitoring and alerting mechanisms, the system maintains reliability and provides timely notifications to ensure the integrity of the data processing pipeline.

---


