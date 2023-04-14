import logging
import asyncio
import interactions
from interactions import Client, Intents, listen, Task, IntervalTrigger
from interactions.ext import prefixed_commands

from bot.bot_status import ServerState

from config import config
from logger import logger


@listen()
async def on_startup():
    await update_presence_schedule()


@listen()
async def on_ready():
    logger.info("Ready")
    logger.info(f"This bot is owned by {bot.owner}")


@Task.create(IntervalTrigger(minutes=1))
async def update_presence_schedule():
    logger.debug("update presence")
    await state.update_presence()


if __name__ == "__main__":
    logging.basicConfig()
    cls_log = logging.getLogger(interactions.const.logger_name)
    cls_log.setLevel(logging.ERROR)

    bot = Client(intents=Intents.DEFAULT, sync_interactions=True, asyncio_debug=True, logger=cls_log)
    prefixed_commands.setup(bot)
    state = ServerState(bot)

    bot.load_extension("commands.indigo")
    discord_token = config['DISCORD']['token']
    try:
        bot.start(discord_token)
        logger.info("bot is start")
    except Exception as e:
        logging.error(e)
