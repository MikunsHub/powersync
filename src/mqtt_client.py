import ssl
import time
import json
import signal
import logging
import paho.mqtt.client as mqtt
from transform import transform_payload
from prometheus_client import Summary, Counter

logger = logging.getLogger(__name__)



class MQTTClient:
    """
    MQTT client that connects to a broker and subscribes to a topic for receiving MQTT messages.

    Args:
        host (str): MQTT broker host address.
        port (int): MQTT broker port number.
        ca_file (str): Path to the CA file for TLS/SSL.
        username (str): MQTT broker username.
        password (str): MQTT broker password.
        topic (str): MQTT topic to subscribe to.
        max_retries (int): Maximum number of connection retry attempts on failure.
        retry_interval (int): Time interval (in seconds) between connection retry attempts.
    """

    def __init__(
        self,
        host,
        port,
        ca_file,
        username,
        password,
        topic,
        max_retries=5,
        retry_interval=10,
    ):
        self.client = mqtt.Client()
        self.client.username_pw_set(username, password)
        self.client.tls_set(ca_certs=ca_file, cert_reqs=ssl.CERT_REQUIRED)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.host = host
        self.port = port
        self.topic = topic

        self.max_retries = max_retries
        self.retry_interval = retry_interval

        self.error_counter = Counter('error_count', 'Number of errors')
        self.processing_time = Summary(
            "message_processing_time", "Time spent processing messages"
        )
        self.message_counter = Counter(
            "message_throughput_total", "Total number of received messages"
        )

        signal.signal(signal.SIGINT, self.handle_shutdown)

    def on_connect(self, client, userdata, flags, rc):
        """
        Callback function executed when the client connects to the MQTT broker.

        Args:
            client: The MQTT client instance.
            userdata: The user data passed when connecting.
            flags: Response flags from the broker.
            rc (int): Result code indicating the success of the connection.
        """
        try:
            if rc == 0:
                logger.info("Connected to MQTT broker")
                client.subscribe(self.topic)
                logger.info(f"Subscribed to {self.topic}")
            else:
                logger.error("Connection failed with code: %s", rc)
                self.error_counter.inc()
        except Exception as e:
            logger.error("An error occurred in on_connect: %s", e)
            self.error_counter.inc()

    def on_message(self, client, userdata, msg):
        """
        Callback function executed when a new message is received on the subscribed topic.

        Args:
            client: The MQTT client instance.
            userdata: The user data passed when connecting.
            msg: The received message object.
        """
        try:
            # Record starting time
            start_time = time.time()

            # Transform Payload and return
            transformed_payload = transform_payload(msg.payload)
            print("transformed=", json.dumps(transformed_payload, indent=2))

            # Measure and observe processing time
            self.processing_time.observe(time.time() - start_time)

            # Increment message counter
            self.message_counter.inc()
        except Exception as e:
            logger.error("An error occurred in on_message: %s", e)
            self.error_counter.inc()

    def connect(self):
        """
        Connects to the MQTT broker with retry mechanism.
        """
        retries = 0
        while retries < self.max_retries:
            try:
                self.client.connect(self.host, self.port)
                logger.info("Connected to MQTT broker")
                return
            except Exception as e:
                logger.error(
                    "Connection attempt %d to %s:%d failed: %s",
                    retries + 1,
                    self.host,
                    self.port,
                    e,
                )
                retries += 1
                self.error_counter.inc()
                time.sleep(self.retry_interval)

        logger.error("Failed to connect after %d attempts. Exiting.", self.max_retries)
        self.error_counter.inc()
        exit()

    def loop_forever(self):
        """
        Starts the MQTT client's loop to listen for incoming messages.
        """
        try:
            self.client.loop_forever()
        except (KeyboardInterrupt, Exception) as e:
            logger.info("Shutting down gracefully...")
            self.client.disconnect()
            logger.info("Disconnected from MQTT broker.")

    def handle_shutdown(self, signum, frame):
        """
        Gracefully handles the shutdown signal by disconnecting from the MQTT broker.
        """
        logger.info("Received signal for graceful shutdown")
        self.client.disconnect()
        logger.info("Disconnected from MQTT broker.")
        exit()
