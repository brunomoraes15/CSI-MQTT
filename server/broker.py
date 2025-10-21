import os
import json
import time
from dotenv import load_dotenv
from paho.mqtt import client as mqtt
from general.logging import logger


class MQTT_Broker:

    def __init__(self, broker_ip, broker_port, topic, save_dir):
        self.broker_ip = broker_ip
        self.broker_port = int(broker_port)
        self.topic = topic
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

        self.client = mqtt.Client(client_id="ServerListener")
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, rc):
        if rc == 0:
            logger.info(f"Connected to MQTT broker at {self.broker_ip}:{self.broker_port}")
            client.subscribe(self.topic)
            logger.info(f"Subscribed to topic: {self.topic}")
        else:
            logger.error(f"Failed to connect. Return code: {rc}")

    def _on_message(self, msg):
        try:
            payload = json.loads(msg.payload.decode())
            filename = payload.get("filename", f"data_{int(time.time())}.csv")
            data = payload.get("data", "")
            filepath = os.path.join(self.save_dir, filename)
            with open(filepath, "w") as f:
                f.write(data)
            logger.info(f"Saved file: {filepath}")
        except Exception as e:
            logger.exception(f"Error processing message: {e}")

    def _on_disconnect(self, rc):
        if rc != 0:
            logger.warning("Unexpected disconnection")
            self._reconnect()

    def connect(self):
        try:
            logger.info(f"Connecting to {self.broker_ip}:{self.broker_port} ...")
            self.client.connect(self.broker_ip, self.broker_port, keepalive=60)
            self.client.loop_start()
        except Exception as e:
            logger.exception(f"Error connecting to broker: {e}")

    def _reconnect(self):
        while True:
            try:
                time.sleep(5)
                self.client.reconnect()
                logger.info("Reconnected successfully.")
                break
            except Exception:
                logger.warning("Reconnect failed, retrying...")
                time.sleep(5)

    def run_forever(self):
        try:
            self.connect()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("MQTT_Broker stopped by user.")
        finally:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("MQTT client disconnected cleanly.")
