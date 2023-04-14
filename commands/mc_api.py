import socket

from paramiko import SSHClient, AutoAddPolicy
from mcrcon import MCRcon

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
        # self.mcr = MCRcon(self.mcr_addr, self.mcr_pass, port=self.mcr_port,
        #                   tlsmode=0, timeout=5)

    def mc_connect(self):
        try:
            self.mcr.connect((self.mcr_addr, self.mcr_port))
        except Exception as e:
            logger.error(e)
        finally:
            self.mcr.close()

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
        self.ssh_connect()

        CMD = "/bin/bash /home/ubuntu/mod/boot start"
        stdin, stdout, stderr = self.client.exec_command(CMD)

        logger.info(self.res_stdout(stdout))
        logger.error(self.res_stderr(stderr))

        self.client.close()

    def stop_mc(self):
        self.ssh_connect()

        CMD = "/bin/bash /home/ubuntu/mod/boot stop"
        stdin, stdout, stderr = self.client.exec_command(CMD)

        logger.info(self.res_stdout(stdout))
        logger.error(self.res_stderr(stderr))

        self.client.close()
