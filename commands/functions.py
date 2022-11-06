import disnake, time, asyncio
from disnake.ext import commands

from .system._dataReceiver import DataReceiver
from .system._programReceiver import ProgramReceiver
from .system._embed import Embeds
from .modal._textInput import ErrorNotice

class Functions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #! Commands !#
    @commands.slash_command(name = "오류제보", description = "오류가 발견되었나요? 여기로 제보해주세요!")
    async def errorNotice(self, ctx):
        await ctx.response.send_modal(modal = ErrorNotice(self.bot))