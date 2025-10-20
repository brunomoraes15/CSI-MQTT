from dotenv import load_dotenv
from broker import MQTT_Broker
import os

if __name__ == "__main__":
    load_dotenv("venv/credentials.env")

    broker_ip = os.getenv("BROKER", "localhost")
    broker_port = os.getenv("REMOTE_PORT", 1883)
    topic = os.getenv("TOPIC", "rasp/+/data")
    save_dir = os.getenv("SERVER_DIR", "/home/csi/COLETA-TESTE")

    broker = MQTT_Broker(broker_ip, broker_port, topic, save_dir)
    broker.run_forever()
