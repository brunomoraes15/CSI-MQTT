import time, json, os
from paho.mqtt import client as mqtt
from general.logging import logger

class MQTT_Publish:
    def __init__(self, client_id, server_ip, port, username=None, password=None, topic=None):
        self.client = mqtt.Client(
            client_id=client_id,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION1
        )
        self.topic = topic
        self.client.username_pw_set(username, password)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        self.server_ip = server_ip
        self.port = port
        
    def on_connect(self, client, userdata, flags, rc):
            if rc == 0:
                logger.info(" Connected successfully to MQTT broker.")
            else:
                logger.error(f" Connection failed. Code: {rc}")

    def on_disconnect(self, client, userdata, rc):
            logger.warning(f" Disconnected from MQTT broker. Code: {rc}")

    def connect(self):
            logger.info(f"Connecting to {self.server_ip}:{self.port} ...")
            self.client.connect(self.server_ip, self.port, keepalive=60)
            self.client.loop_start()

    def data_publish(self, dir_path):
            try:
                if not os.path.isdir(dir_path):
                    logger.error(f"Directory not found: {dir_path}")
                    return
                
                csv_files = sorted([f for f in os.listdir(dir_path) if f.lower().endswith(".csv")])

                if not csv_files:
                    logger.warning("No CSV")
                    return
                
                for filename in csv_files:
                    file_path = os.path.join(dir_path, filename)
                    try:
                        with open(file_path, "r") as file:
                            csv_data =  file.read()

                            csv_payload = {
                                "filename": filename,
                                "data": csv_data,
                                "timestamp": time.time()
                            }

                            result = self.client.publish(self.topic, json.dumps(csv_payload), qos=1)
                            result.wait_for_publish()

                            if result.is_published():
                                logger.info(f" Published '{filename}' to topic '{self.topic}' successfully.")
                                sent_dir = os.path.join(dir_path, "sent_to_server")
                                os.makedirs(sent_dir, exist_ok=True)
                                os.rename(file_path, os.path.join(sent_dir, filename))
                                logger.info(f" Moved '{filename}' to '{sent_dir}'")
                            else:
                                logger.error(f" Failed to publish '{filename}'.")

                    except Exception as e:
                        logger.exception(f"Error while parsing csv")

            except Exception as e:
                logger.exception(f"Unexpected error while publishing data to server {server_ip}: {e}")
    
    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        logger.info("MQTT client disconnected.")



import os
import time
from dotenv import load_dotenv
from general.logging import logger


load_dotenv(dotenv_path="venv/credentials.env")

server_ip = os.getenv("SERVER_IP")
#username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
remote_port = int(os.getenv("REMOTE_PORT", 1884))
topic = os.getenv("TOPIC")
client_id = os.getenv("CLIENT_ID")
#csv_path = os.getenv("CSV_PATH", "ESP_Esteira_Teste/004-01.csv")
interval = int(os.getenv("SEND_INTERVAL", 1))  #

username = "csi"

logger.info(f"server IP: {server_ip}")
logger.info(f"client ID: {client_id}")
logger.info(f"username: {username or username}")
logger.info(f"password: {'*' * len(password) if password else 'None'}")
logger.info(f"remote port: {remote_port}")
logger.info(f"topic: {topic}")
#logger.info(f"csv path: {csv_path}")
logger.info(f"send interval: {interval}s")

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
            publisher.data_publish("path")
            time.sleep(interval)

    except KeyboardInterrupt:
        logger.info(" Stopping CSV sender...")
    finally:
        publisher.disconnect()
