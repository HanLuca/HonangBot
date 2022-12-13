import disnake, time, asyncio, random
from disnake.ext import commands

from .system._dataReceiver import DataReceiver
from .system._programReceiver import ProgramReceiver
from .system._embed import Embeds

class EconomyData(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name = "도박", description = "Honang 봇에서 도박을 즐겨보세요!")
    async def randomCoinpoint(self, ctx, betting : int = 1000):
        await ctx.response.defer(); await asyncio.sleep(1)

        #! Variables !#
        basicPath = f"USERDATA/{ctx.author.id}"
        percentRandom = 30 if DataReceiver.get(basicPath, "1_Points") >= 500000 else 50

        if DataReceiver.check(ctx.author.id) == False: 
            await ctx.edit_original_response(embed = ProgramReceiver.embedError(f"\❓{ctx.author.mention} 님의 계정이 존재하지 않습니다.\n**`/계정생성`** 명령어를 통해 가입해주세요.", ctx.author))

        elif betting > 100000 or betting <= 0 or DataReceiver.get(basicPath, "1_Points") < betting:
            await ctx.edit_original_response(embed = ProgramReceiver.embedError("\❓입력한 배팅금액이 올바르지 않습니다.", ctx.author))

        else:
            userCpt = DataReceiver.get(basicPath, "1_Points")
            userLevel = DataReceiver.get(basicPath, "2_Level")
            userExp = DataReceiver.get(basicPath, "3_Expoints")

            randomResult = random.randrange(1, 101)
            randomExp = random.randrange(1, 5)

            if randomResult <= percentRandom:
                DataReceiver.update(basicPath, {"1_Points" : int(userCpt + betting * 2)})
                if int(userExp + randomExp) >= userLevel * 1000:
                    DataReceiver.update(basicPath, {"3_Expoints" : 0}); Expoint = userLevel * 1000
                    DataReceiver.update(basicPath, {"2_Level" : int(userLevel + 1)})

                else:
                    Expoint = int(userExp + randomExp)
                    DataReceiver.update(basicPath, {"3_Expoints" : int(Expoint)})

                embed = disnake.Embed(description = Embeds.embedBetting_Success(ctx.author, betting, int(userCpt + betting * 2), randomExp, Expoint, userLevel), color = disnake.Color.green())
                ProgramReceiver.embedFooter(embed, ctx.author)

                await ctx.edit_original_response(embed = embed)

            else:
                DataReceiver.update(basicPath, {"1_Points" : int(userCpt - betting)})

                embed = disnake.Embed(description = Embeds.embedBetting_Fail(ctx.author, betting, int(userCpt - betting)), color = disnake.Color.red())
                ProgramReceiver.embedFooter(embed, ctx.author)

                await ctx.edit_original_response(embed = embed)

    @commands.slash_command(name = "채집", description = "Cpt 를 모아보세요!")
    async def randomCoinpoint(self, ctx):
        await ctx.response.defer(); await asyncio.sleep(1)

        await ctx.edit_original_response("개발중인 기능입니다!")