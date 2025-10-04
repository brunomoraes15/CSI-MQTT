from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
import time, sys, os

load_dotenv()  

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
    
    def start_tunnel(self) -> bool:
        try:
            self.tunnel = SSHTunnelForwarder(
                (self.server_ip, self.default_port),
                ssh_username = self.ssh_user,
                ssh_password = self.ssh_password,
                remote_bind_address=('127.0.0.1', self.remote_port),
                local_bind_address=('127.0.0.1', self.local_port),
            )
            self.tunnel.start()
            print(f"SSH tunnel established: localhost:{self.local_port} → {self.server_ip}:{self.remote_port}")

        except Exception as e:
            print(f"Failed to start SSH tunnel or run command: {e}")
            sys.exit(1)

    def main(self): # edição futura
        try:
            self.start_tunnel()
            print(" Connection established and ready.")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nInterrupted by user.")
        except Exception as e:
            print(f"Error during SSH operation: {e}")
        finally:
            self.tunnel.stop()

if __name__ == "__main__":
    SERVER_IP = os.environ.get("SSH_SERVER_IP")
    USER = os.environ.get("SSH_USER")
    PASSWORD = os.environ.get("SSH_PASSWORD")
    REMOTE_PORT = int(os.environ.get("REMOTE_MQTT_PORT", 1883))
    LOCAL_PORT = int(os.environ.get("LOCAL_MQTT_PORT", 1883))

    connection = SSH_Connection(
        server_ip=SERVER_IP,
        ssh_user=USER,
        ssh_password=PASSWORD,
        remote_port=REMOTE_PORT,
        local_port=LOCAL_PORT
    )
    connection.main()