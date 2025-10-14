from paho.mqtt import client as mqtt
import json
import os
import time

# Configuration
BROKER = "localhost"   
PORT = 1884
TOPIC = "rasp/+/data"  
SAVE_DIR = "/home/csi/COLETA-TESTE"

# E
#os.makedirs(SAVE_DIR, exist_ok=True)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(" Connected to MQTT broker")
        client.subscribe(TOPIC)
        print(f" Subscribed to topic: {TOPIC}")
    else:
        print(f" Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        filename = payload.get("filename", f"data_{int(time.time())}.csv")
        csv_data = payload.get("data", "")
        filepath = os.path.join(SAVE_DIR, filename)

        with open(filepath, "w") as f:
            f.write(csv_data)

        print(f" Saved file: {filepath}")

    except Exception as e:
        print(f" Error processing message: {e}")

try:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_forever()

except KeyboardInterrupt:
        print("Closed server connection")

