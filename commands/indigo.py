from interactions import Extension
from interactions import slash_command, slash_option, OptionType, SlashCommandChoice
from interactions import InteractionContext
from logger import logger

from commands.indigo_api import IndigoApi


indigo = IndigoApi()


class IndigoCommand(Extension):
    @slash_command(name="indigo", description="Indigoサーバーの状態を更新")
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
    async def indigo(self, ctx: InteractionContext, **kwargs):
        logger.info(f"receive indigo command: {ctx.command.name}")
        prog_message = await ctx.send("処理中...")
        kwargs = ctx.kwargs
        logger.info(kwargs)
        if kwargs["state"] == "on":
            message = indigo.start_server()
            # server_state.indigo = True
            await prog_message.edit(content=message)
        elif kwargs["state"] == "off":
            message = indigo.stop_server()
            # server_state.indigo = False
            await prog_message.edit(content=message)
        elif kwargs["state"] == "update":
            state = indigo.update_status()
            text = "更新が完了しました:"
            if state is True:
                print("server is up")
                text += "Indigoサーバーは起動しています。"
                # server_state.indigo = True
            elif state is False:
                print("server is down")
                text += "Indigoサーバーは停止しています。"
                # server_state.indigo = False
            await prog_message.edit(content=text)
        # await server_state.update_presence()
        return True

    @indigo.error
    async def indigo_error(self, e, *args, **kwargs):
        logger.error(f"indigo hit error with {args=}, {kwargs=}")
        logger.error(e)
