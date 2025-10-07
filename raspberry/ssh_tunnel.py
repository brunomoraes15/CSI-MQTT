from sshtunnel import SSHTunnelForwarder
import paramiko
import time, sys, os
from general.logging import logger
import subprocess


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
        self.input = None

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
    #debug
    def run_local_command(self, command):
        try:
            process = subprocess.Popen(command, shell=True)
            process.wait()
        except Exception as e:
            logger.error(f"Error while executing '{command}': {e}")
    #debug
    def run_remote_command(self, command):
        
        if not self.client:
            logger.error("no active SSH session thus cannot execute command")
            return
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
        except Exception as e:
            logger.error(f"Error while executing '{command}': {e}")

    def execution_debug(self):
        try:
            self.start_tunnel()
            logger.info("Connection established and ready.")
            while (self.client or self.tunnel):
                self.input = input("> ")
                self.run_local_command(self.input)
        except KeyboardInterrupt:
            logger.warning("Operation interrupted by user.")
        except Exception as e:
            logger.critical(f"Fatal error during SSH operation: {e}")
        #finally:
            #self.stop_tunnel()


