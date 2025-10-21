from dotenv import load_dotenv
from broker import MQTT_Broker
import os


load_dotenv("venv/credentials.env")

broker_ip = os.getenv("BROKER")
broker_port = os.getenv("REMOTE_PORT")
topic = os.getenv("TOPIC")
save_dir = os.getenv("SERVER_DIR")

broker = MQTT_Broker(broker_ip, broker_port, topic, save_dir)
broker.run_forever()
