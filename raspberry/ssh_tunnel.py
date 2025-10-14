from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
import paramiko
import time, sys, os
from general.logging import logger


class SSH_Connection:
    def __init__(self, server_ip, ssh_user, ssh_password, remote_port, local_port):
        self.server_ip = server_ip
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.remote_port = remote_port
        self.local_port = local_port
        self.default_port = 22
        self.tunnel = None
        self.client = None

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

        
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.server_ip, username=self.ssh_user, password=self.ssh_password)
            logger.info("SSH client connected successfully.")

        except Exception as e:
            logger.error(f"Failed to start SSH tunnel or client: {e}")
            raise  

    def stop_tunnel(self):
        if self.client:
            self.client.close()
            logger.info("SSH client closed.")
        if self.tunnel and self.tunnel.is_active:
            self.tunnel.stop()
            logger.warning("SSH tunnel closed.")
        else:
            logger.warning("No active SSH tunnel to close.")

    def run_command(self, command="hostnamectl"):
        """Executa um comando remoto via SSH (requer conexão ativa)."""
        if not self.client:
            logger.error("No active SSH session. Cannot execute command.")
            return

        try:
            logger.info(f"Executing '{command}' on {self.server_ip}...")
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()

            if output:
                logger.info(f"Command output:\n{output}")
            if error:
                logger.error(f"Command error:\n{error}")

        except Exception as e:
            logger.error(f"Error while executing '{command}': {e}")

    def main(self):
        try:
            self.start_tunnel()
            logger.info("Connection established and ready.")
            self.run_command("hostnamectl")
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