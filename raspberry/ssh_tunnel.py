from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
from config import *
import time, sys, os

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
                ssh_username = self.ssh_user,
                ssh_password = self.ssh_password,
                remote_bind_address=('127.0.0.1', self.remote_port),
                local_bind_address=('127.0.0.1', self.local_port),
            )
            self.tunnel.start()
            print(f"{msg_ok} SSH tunnel established: localhost:{self.local_port} → {self.server_ip}:{self.remote_port}")

        except Exception as e:
            print(f"{msg_error} Failed to start SSH tunnel or run command: {e}")
            sys.exit(1)

    def stop_tunnel(self):
        if self.tunnel and self.tunnel.is_active:
            self.tunnel.stop()
            print(f"{msg_warning} ssh tunnel closed")
        else:
            print(f"{msg_warning} no active ssh tunnel to close")

    def main(self): # edição futura
        try:
            self.start_tunnel()
            print(f"{msg_ok} connection established and ready")

        except KeyboardInterrupt:
            print("\noperation interrupted by user")

        except Exception as e:
            print(f"{msg_error} fatal error during ssh operation: {e}")
        finally:
            self.stop_tunnel()

if __name__ == "__main__":
    load_dotenv(dotenv_path="venv/credentials.env")
    SERVER_IP = os.getenv("SSH_SERVER_IP")
    USER = os.getenv("SSH_USER")
    PASSWORD = os.getenv("SSH_PASSWORD")
    REMOTE_PORT = int(os.getenv("REMOTE_PORT", 1883))
    LOCAL_PORT = int(os.getenv("LOCAL_PORT", 1883))

    print(f"{msg_info} server IP:", SERVER_IP)
    print(f"{msg_info} user:", USER)
    print(f"{msg_info} password:", PASSWORD)
    print(f"{msg_info} remote port:", REMOTE_PORT)
    print(f"{msg_info} local port:", LOCAL_PORT)
    
    connection = SSH_Connection(
        server_ip=SERVER_IP,
        ssh_user=USER,
        ssh_password=PASSWORD,
        remote_port=REMOTE_PORT,
        local_port=LOCAL_PORT
    )
    connection.main()