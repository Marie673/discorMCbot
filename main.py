import logging
from configparser import ConfigParser

import interactions
from interactions import Client, Intents, listen
from interactions.ext import prefixed_commands


@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


if __name__ == "__main__":
    logging.basicConfig()
    cls_log = logging.getLogger(interactions.const.logger_name)
    cls_log.setLevel(logging.ERROR)

    config = ConfigParser()
    config.read("config.ini")

    bot = Client(intents=Intents.DEFAULT, sync_interactions=True, asyncio_debug=True, logger=cls_log)
    prefixed_commands.setup(bot)

    # bot.load_extension("mine_bot")
    discord_token = config['DISCORD']['token']
    bot.start(discord_token)

