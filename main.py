import os
import time
import environ
from mqtt_client import MQTTClient
from config_logging import configure_logging 
from prometheus_client import start_http_server

# Configure logging
configure_logging()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Load environment variables from .env file
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

host = env("HOST")
port = int(env("PORT"))
ca_file = "ca-stage.crt"
username = env("USERNAME")
password = env("PASSWORD")
topic = env("TOPIC")

# Initialize and configuring the MQTT client
mqtt_client = MQTTClient(host, port, ca_file, username, password, topic)
mqtt_client.connect()
mqtt_client.loop_forever()

# Starting Prometheus 
start_http_server(9090)