import logging
from logger import logger
import interactions
from interactions import Client, Intents


class ServerState:
    def __init__(self):
        self.indigo = None
        self.mc = None
        self.bot = bot

    async def update_presence(self):
        act: str = "Indigo: "
        if self.indigo:
            act += "UP"
        else:
            act += "DOWN"
        act += " | MC: "
        if self.mc:
            act += "UP"
        else:
            act += "DOWN"
        act += "     "
        logger.info(act)
        await self.bot.change_presence(activity=act)


logging.basicConfig()
cls_log = logging.getLogger(interactions.const.logger_name)
cls_log.setLevel(logging.ERROR)
bot = Client(intents=Intents.DEFAULT, sync_interactions=True, asyncio_debug=True, logger=cls_log)
server_state = ServerState()

