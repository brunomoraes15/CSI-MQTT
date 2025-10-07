from dotenv import load_dotenv
from .ssh_tunnel import SSH_Connection
import os
from general.logging import logger

load_dotenv(dotenv_path="venv/credentials.env")

server_ip = os.getenv("SSH_SERVER_IP")
user = os.getenv("SSH_USER")
password = os.getenv("SSH_PASSWORD")
remote_port = int(os.getenv("REMOTE_PORT", 1883))
local_port = int(os.getenv("LOCAL_PORT", 1883))

logger.info(f"server IP: {server_ip}")
logger.info(f"user: {user}")
logger.info(f"password: {'*' * len(password) if password else 'None'}")
logger.info(f"remote port: {remote_port}")
logger.info(f"local port: {local_port}")

connection = SSH_Connection(
        server_ip=server_ip,
        ssh_user=user,
        ssh_password=password,
        remote_port=remote_port,
        local_port=local_port
    )
#connection.execution_debug()