import sys
import logging

logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s [%(levelname)s] %(message)s",  
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("logs/ssh_connection.log"),  
        logging.StreamHandler(sys.stdout)       
    ]
)
logger = logging.getLogger(__name__)
