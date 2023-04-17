import requests
from ping3 import ping
import time

from bot_client import server_state

from config import config
from logger import logger


class IndigoApi:
    def __init__(self):
        self.api_id = config['INDIGO']['API_ID']
        self.api_secret_key = config['INDIGO']['API_SECRET_KEY']
        self.accessToken = None

        self.minecraft_instance_name = config['INSTANCE']['MC_INSTANCE_NAME']
        self.minecraft_instance_id = None
        self.minecraft_instance_address = config['INSTANCE']['address']

        self.expiresIn = None
        self.issuedAt = None

        self.start()
        self.get_mc_instance_ids()

    def start(self):
        headers = {"Content-Type": "application/json"}
        data = {"grantType": "client_credentials",
                "clientId": self.api_id,
                "clientSecret": self.api_secret_key,
                "code": ""}
        response = requests.post('https://api.customer.jp/oauth/v1/accesstokens', headers=headers, json=data)

        if response.status_code == 201:
            data = response.json()
            self.accessToken = data['accessToken']
            self.expiresIn = float(data['expiresIn'])
            self.issuedAt = float(data['issuedAt'])
            logger.debug(f"access Token: {self.accessToken}")
            logger.debug(f"expiresIn: {self.expiresIn}")
            logger.debug(f"issuedAt: {self.issuedAt}")
            return
        else:
            logger.error(str(response.status_code) + ":" + response.text)
            raise "Oauth failed"

    def check_exp(self):
        now_time = time.time() * 1000
        logger.debug(now_time)
        logger.debug(str(self.issuedAt + self.expiresIn) + ":" + str(self.issuedAt) + ":" + str(self.expiresIn))
        if now_time >= self.issuedAt + self.expiresIn:
            self.start()

    def get_mc_instance_ids(self):
        self.check_exp()

        headers = {"Authorization": f"Bearer {self.accessToken}"}
        response = requests.get("https://api.customer.jp/webarenaIndigo/v1/vm/getinstancelist", headers=headers)

        if response.status_code == 200:
            data = response.json()
            for instance in data:
                if self.minecraft_instance_name == instance['instance_name']:
                    self.minecraft_instance_id = instance['id']
                    logger.debug(f"Minecraft Instance ID is {self.minecraft_instance_id}")
                    return
            raise "Not found MC instance"
        raise "invalid request"

    def start_server(self):
        self.check_exp()

        headers = {"Authorization": f"Bearer {self.accessToken}"}
        data = {
            "instanceId": f"{self.minecraft_instance_id}",
            "status": "start"
        }
        response = requests.post("https://api.customer.jp/webarenaIndigo/v1/vm/instance/statusupdate",
                                 headers=headers, json=data)

        if response.status_code == 200:
            logger.info("server started.")
            server_state.indigo = True
            return "サーバーが起動しました"
        elif response.status_code == 400:
            server_state.indigo = True
            return "サーバーはすでに起動しています"
        else:
            server_state.indigo = None
            return response.text

    def stop_server(self):
        self.check_exp()

        headers = {"Authorization": f"Bearer {self.accessToken}"}
        data = {
            "instanceId": f"{self.minecraft_instance_id}",
            "status": "stop"
        }
        response = requests.post("https://api.customer.jp/webarenaIndigo/v1/vm/instance/statusupdate",
                                 headers=headers, json=data)

        if response.status_code == 200:
            logger.info("server stopped.")
            server_state.indigo = False
            return "サーバーが停止しました"
        elif response.status_code == 400:
            server_state.indigo = False
            return "サーバーはすでに停止しています"
        else:
            server_state.indigo = None
            return response.text

    def update_status(self):
        res = ping(self.minecraft_instance_address, timeout=2)
        if res is None:
            server_state.indigo = False
            return False
        else:
            server_state.indigo = True
            return True
