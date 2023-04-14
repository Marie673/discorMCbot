from interactions import Extension
from interactions import slash_command, slash_option, OptionType, SlashCommandChoice
from interactions import InteractionContext
from logger import logger

from bot_client import server_state
from commands.mc_api import McApi

mc = McApi()


class McCommand(Extension):
    @slash_command(name="mc", description="Minecraftサーバーの状態を更新")
    @slash_option(
        name="state",
        description="起動: on、停止: off、更新: update",
        required=True,
        opt_type=OptionType.STRING,
        choices=[
            SlashCommandChoice(name="on", value="on"),
            SlashCommandChoice(name="off", value="off"),
            SlashCommandChoice(name="update", value="update")
        ]
    )
    async def mc(self, ctx: InteractionContext, **kwargs):
        logger.info(f"receive indigo command: {ctx.command.name}")
        prog_message = await ctx.send("処理中...")
        kwargs = ctx.kwargs
        logger.info(kwargs)
        if kwargs["state"] == "on":
            mc.start_mc()
            # server_state.mc = True
            await prog_message.edit(content="起動が完了しました")
        elif kwargs["state"] == "off":
            mc.stop_mc()
            # server_state.mc = False
            await prog_message.edit(content="停止が完了しました")
        elif kwargs["state"] == "update":
            res = mc.mc_connect()
            if res is True:
                await prog_message.edit(content="マイクラサーバーは起動しています")
            else:
                await prog_message.edit(content="マイクラサーバーは起動していません")
        await server_state.update_presence()
        return True

    @mc.error
    async def mc_error(self, e, *args, **kwargs):
        print(f"indigo hit error with {args=}, {kwargs=}")
        print(e)


def setup(bot):
    McCommand(bot)
