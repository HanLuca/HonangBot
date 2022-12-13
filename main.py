import disnake, os, time, asyncio
from disnake.ext import commands
from dotenv import load_dotenv

#! Basic Import #!
from commands.system._dataReceiver import DataReceiver
from commands.system._programReceiver import ProgramReceiver

#! File Import !#
from commands.userData import UserData
from commands.coinData import CoinData
from commands.economyData import EconomyData
from commands.functions import Functions

#! Data Receiver !#
load_dotenv()
token = os.getenv("TOKEN")

bot = commands.Bot (
    command_prefix = ["<@1029323692464951398> ", "!! "],
    intents = disnake.Intents.all()
    # test_guilds = [1028908853162688572]
)
bot.add_cog(UserData(bot))
bot.add_cog(CoinData(bot))
bot.add_cog(EconomyData(bot))
bot.add_cog(Functions(bot))

#! File !#
@bot.event
async def on_ready():
    activity = disnake.Game(name = "[ V - 0.02 ] 탄생중입니다 😓", type = 2)
    await bot.change_presence(status = disnake.Status.idle, activity = activity)

    member = await bot.fetch_user("869582271387148312"); os.system("cls"); print("Start")

    try: DataReceiver.get("SYSTEM", "1_UserAmount")
    except: DataReceiver.update("SYSTEM", {"1_UserAmount" : 0}); print("재 실행이 필요함")
    else:
        embed = disnake.Embed (
            description = f"""
            **봇이 가동되었습니다.**    

            **┌────── [ 가동 정보 ] ──────┐**
            \
            \🕐 <t:{round(time.time())}:R> 에 가동됨
            \😁 {DataReceiver.get("SYSTEM", "1_UserAmount")} 명의 유저
            """,
            color = 0x2f3136
        )
        await member.send(embed = embed)

    await asyncio.sleep(3600); os.system("python main.py")

bot.run(token)