import sys, os, logging

os.makedirs("general/logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s [%(levelname)s] %(message)s",  
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("general/logs/mqtt.log", encoding="utf-8"), 
        logging.StreamHandler(sys.stdout)
        ]
    )
logger = logging.getLogger("MQTT")
