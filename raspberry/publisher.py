import time, json, os
from paho.mqtt import client as mqtt
from general.logging import logger

class MQTT_Publish:
    def __init__(self, client_id, server_ip, port, topic=None):
        self.client = mqtt.Client(
            client_id=client_id,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION1
        )
        self.topic                = topic
        self.client.on_connect    = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.server_ip            = server_ip
        self.port                 = port
        
    def on_connect(self, client, userdata, flags, rc):
            if rc == 0:
                logger.info(" Connected successfully to MQTT broker.")
            else:
                logger.error(f" Connection failed. Code: {rc}")

    def on_disconnect(self, client, userdata, rc):
            logger.warning(f" Disconnected from MQTT broker. Code: {rc}")

    def connect(self):
            logger.info(f"Connecting to {self.server_ip}:{self.port}")
            self.client.connect(self.server_ip, self.port, keepalive=60)
            self.client.loop_start()

    def data_publish(self, dir_path):
            try:
                if not os.path.isdir(dir_path):
                    logger.error(f"Directory not found: {dir_path}")
                    return
                
                csv_files = sorted([f for f in os.listdir(dir_path) if f.lower().endswith(".csv")])

               # if not csv_files:
               #     logger.warning("No CSV")
               #     return
                
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
                logger.exception(f"Unexpected error while publishing data to server {self.server_ip}: {e}")
    
    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        logger.info("MQTT client disconnected.")



