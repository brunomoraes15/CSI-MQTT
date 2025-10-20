from general.logging import logger
from raspberry.publisher import MQTT_Publish
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="venv/credentials.env")

server_ip = os.getenv("SERVER_IP")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
remote_port = int(os.getenv("REMOTE_PORT", 1883))
topic = os.getenv("TOPIC")
client_id = os.getenv("CLIENT_ID")
interval = int(os.getenv("SEND_INTERVAL", 1))
csv_dir = os.getenv("CSV_PATH")


logger.info(f"server IP: {server_ip}")
logger.info(f"client ID: {client_id}")
logger.info(f"username: {username or username}")
logger.info(f"password: {'*' * len(password) if password else 'None'}")
logger.info(f"remote port: {remote_port}")
logger.info(f"topic: {topic}")
logger.info(f"csv path: {csv_dir}")

if __name__ == "__main__":
    publisher = MQTT_Publish(
        client_id=client_id,
        server_ip=server_ip,
        port=remote_port,
        username=username,
        password=password,
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
