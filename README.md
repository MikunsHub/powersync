# PowerSync MQTT Client

The PowerSync MQTT Client is a Python application designed to connect to an MQTT broker, subscribe to a specific topic, and process incoming messages. It transforms and logs the received data while providing robust error handling and a graceful shutdown mechanism. For a detailed inlook into this project, [architecture.md](architecture.md) goes into details.

## Features

- **MQTT Communication**: Connects to an MQTT broker, subscribes to a specified topic, and receives incoming messages.

- **Data Transformation**: Transforms incoming MQTT payload data from JSON format to a structured format, providing a clean and organized representation.

- **Robust Error Handling**: Implements error handling for connection failures, message processing errors, and other exceptions, ensuring a smooth operation even in unexpected situations.

- **Configurable Retry Mechanism**: Offers a retry mechanism for establishing a connection to the MQTT broker, with customizable retry attempts and intervals.

- **Graceful Shutdown**: Supports a graceful shutdown mechanism that allows the application to be terminated without data loss or abrupt termination.

- **Logging System**: Has a logging system which provides detailed information about the application's operations, facilitating debugging and monitoring.


## Prerequisites

- Python 3.9+
- Prometheus
- Environ library (`environ`)
- Paho MQTT Client library (`paho-mqtt`)
- MQTT broker's CA file for secure communication
- MQTT broker information (host, port, topic, etc.)

## Local Installation

1. Clone this repository to your local machine.
   
   ```bash
   git clone https://github.com/MikunsHub/powersync.git
   ```

2. Create a virtual environment (recommended).
   
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies.
   
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project directory and fill in the required MQTT broker information.

   ```ini
   HOST=your_mqtt_broker_host
   PORT=your_mqtt_broker_port
   CA_FILE=path_to_ca_file.crt
   USERNAME=your_mqtt_username
   PASSWORD=your_mqtt_password
   TOPIC=your_mqtt_topic
   PROMETHEUS_SERVICE_ADDRESS=your_prometheus_address
   PROMETHEUS_SERVICE_PORT=your_prometheus_port
   ```

5. Run the application.
   
   ```bash
   python src/main.py
   ```

6. Run prometheus.
   
   ```bash
   prometheus --config.file=monitoring/prometheus.yml
   ```

## Docker Installation

1. Clone this repository to your local machine.
   
   ```bash
   git clone https://github.com/MikunsHub/powersync.git
   ```

2. Build the image by running:
   
   ```bash
   docker build -t powersync .
   ```

3. Run the container by:
   
   ```bash
   docker run -e HOST=your_mqtt_broker_host \
           -e PORT=your_mqtt_broker_port \
           -e CA_FILE=path_to_ca_file.crt \
           -e USERNAME=your_mqtt_username \
           -e PASSWORD=your_mqtt_password \
           -e TOPIC=your_mqtt_topic \
           -p 9090:9090 \
           powersync

   ```
   

4. Update the Prometheus Configuration.
   
   ```bash
      global:
         scrape_interval: 15s

      scrape_configs:
         - job_name: 'powersync'
            static_configs:
               - targets: ['docker_container_name_or_ip:9090']

   ```

5. Run prometheus.
   
   ```bash
   docker run -p 9090:9090 -v /monitoring/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus

   ```
To view the metrics of the application with either installation methods, navigate to Prometheus UI by going to http://localhost:9090


## Running Tests

To ensure the reliability and correctness of the PowerSync MQTT Client, tests have been provided. Follow these steps to run the tests:


1. Activate your virtual environment (if you created one) where the required dependencies are installed.

```bash
python -m unittest discover
```
This command will discover and run all the test cases in the test directory.

After running the tests, you will see the test results displayed in the terminal.

## Acknowledgments

This project was created to demonstrate a structured approach to handling MQTT communication and data processing.

## Contributing

Contributions are welcome! Feel free to open issues, submit pull requests, or suggest improvements.



