import logging
import time
from interactions import listen, Task, IntervalTrigger
from interactions.ext import prefixed_commands

from bot_client import bot, server_state

from config import config
from logger import logger


flag = True


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
    await server_state.update_presence()


if __name__ == "__main__":
    prefixed_commands.setup(bot)

    bot.load_extension("commands.indigo")
    bot.load_extension("commands.mc")
    discord_token = config['DISCORD']['token']
    try:
        bot.start(discord_token)
        logger.info("bot is start")
    except KeyboardInterrupt:
        flag = False
        time.sleep(5)
    except Exception as e:
        logging.error(e)
