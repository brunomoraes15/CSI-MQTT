from general.logging import logger
from raspberry.publisher import MQTT_Publish
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="venv/credentials.env")

server_ip = os.getenv("SERVER_IP")
remote_port = int(os.getenv("REMOTE_PORT"))
topic = os.getenv("TOPIC")
client_id = os.getenv("CLIENT_ID")
csv_dir = os.getenv("CSV_PATH")

publisher = MQTT_Publish(
        client_id=client_id,
        server_ip=server_ip,
        port=remote_port,
        topic=topic,
    )

publisher.connect()
try:
    while True:
        publisher.data_publish(csv_dir)

except KeyboardInterrupt:
        logger.info(" Stopping CSV sender")
finally:
    publisher.disconnect()
