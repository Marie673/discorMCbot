import socket
import time

from paramiko import SSHClient, AutoAddPolicy
import threading

from main import flag
from bot_client import server_state

from config import config
from logger import logger


class McApi:
    def __init__(self):
        self.address = config['INSTANCE']['address']
        self.user_name = config['INSTANCE']['user_name']
        self.identity_file = config['INSTANCE']['identity_file']

        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

        self.mcr_addr = config['MCRCON']['address']
        self.mcr_pass = config['MCRCON']['password']
        self.mcr_port = int(config['MCRCON']['port'])
        self.mcr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mcr.settimeout(5)
        # self.mcr = MCRcon(self.mcr_addr, self.mcr_pass, port=self.mcr_port,
        #                   tlsmode=0, timeout=5)

    def mc_connect(self):
        try:
            self.mcr.connect((self.mcr_addr, self.mcr_port))
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            pass

    def ssh_connect(self):
        self.client.connect(
            self.address,
            username=self.user_name,
            key_filename=self.identity_file,
            timeout=5.0
        )

    @staticmethod
    def res_stdout(stdout):
        out = ""
        for line in stdout:
            out += line
        return out

    @staticmethod
    def res_stderr(stderr):
        err = ""
        for line in stderr:
            err += line
        return err

    def start_mc(self):
        try:
            self.ssh_connect()

            CMD = "/bin/bash /home/ubuntu/mod/boot.sh start"
            stdin, stdout, stderr = self.client.exec_command(CMD)

            logger.info(self.res_stdout(stdout))
            logger.error(self.res_stderr(stderr))

        except Exception as e:
            logger.error(e)

        finally:
            self.client.close()

    def stop_mc(self):
        try:
            self.ssh_connect()

            CMD = "/bin/bash /home/ubuntu/mod/boot.sh stop"
            stdin, stdout, stderr = self.client.exec_command(CMD)

            logger.info(self.res_stdout(stdout))
            logger.error(self.res_stderr(stderr))

        except Exception as e:
            logger.error(e)

        finally:
            self.client.close()

    def update_mc(self):
        try:
            self.mc_connect()
            server_state.mc = True
        except Exception as e:
            logger.error(e)
            server_state.mc = False

        self.mcr.close()
