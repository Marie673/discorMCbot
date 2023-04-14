from interactions import Client, Task, IntervalTrigger

from logger import logger


class ServerState:
    def __init__(self, bot: Client):
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
