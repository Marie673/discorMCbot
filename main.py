import logging

import interactions
from interactions import Client, Intents, listen
from interactions.ext import prefixed_commands

from config import config
from logger import logger


@listen()
async def on_ready():
    logger.info("Ready")
    logger.info(f"This bot is owned by {bot.owner}")


if __name__ == "__main__":
    logging.basicConfig()
    cls_log = logging.getLogger(interactions.const.logger_name)
    cls_log.setLevel(logging.ERROR)

    bot = Client(intents=Intents.DEFAULT, sync_interactions=True, asyncio_debug=True, logger=cls_log)
    prefixed_commands.setup(bot)

    bot.load_extension("commands.indigo")
    discord_token = config['DISCORD']['token']
    try:
        bot.start(discord_token)
    except Exception as e:
        logging.error(e)
