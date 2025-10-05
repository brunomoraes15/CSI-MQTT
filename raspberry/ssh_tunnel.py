from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
import time, sys, os
from general.logging import logger

# Autenticação por senha. Trocar para chave ssh posteriomente
class SSH_Connection:
    def __init__(self, server_ip, ssh_user, ssh_password, remote_port, local_port):
        self.server_ip = server_ip
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.remote_port = remote_port
        self.local_port = local_port
        self.tunnel = None
        self.default_port = 22

    def start_tunnel(self):
        try:
            self.tunnel = SSHTunnelForwarder(
                (self.server_ip, self.default_port),
                ssh_username=self.ssh_user,
                ssh_password=self.ssh_password,
                remote_bind_address=('127.0.0.1', self.remote_port),
                local_bind_address=('127.0.0.1', self.local_port),
            )
            self.tunnel.start()
            logger.info(f"SSH tunnel established: localhost:{self.local_port} → {self.server_ip}:{self.remote_port}")
        except Exception as e:
            logger.error(f"Failed to start SSH tunnel or run command: {e}")
            sys.exit(1)

    def stop_tunnel(self):
        if self.tunnel and self.tunnel.is_active:
            self.tunnel.stop()
            logger.warning("SSH tunnel closed.")
        else:
            logger.warning("No active SSH tunnel to close.")

    def main(self):
        try:
            self.start_tunnel()
            logger.info("Connection established and ready.")
        except KeyboardInterrupt:
            logger.warning("Operation interrupted by user.")
        except Exception as e:
            logger.critical(f"Fatal error during SSH operation: {e}")
        finally:
            self.stop_tunnel()

if __name__ == "__main__":
    load_dotenv(dotenv_path="venv/credentials.env")

    server_ip = os.getenv("SSH_SERVER_IP")
    user = os.getenv("SSH_USER")
    password = os.getenv("SSH_PASSWORD")
    remote_port = int(os.getenv("REMOTE_PORT", 1883))
    local_port = int(os.getenv("LOCAL_PORT", 1883))

    logger.info(f"server IP: {server_ip}")
    logger.info(f"user: {user}")
    logger.info(f"password: {'*' * len(password) if password else 'None'}")
    logger.info(f"remote Port: {remote_port}")
    logger.info(f"local Port: {local_port}")

    connection = SSH_Connection(
        server_ip=server_ip,
        ssh_user=user,
        ssh_password=password,
        remote_port=remote_port,
        local_port=local_port
    )
    connection.main()