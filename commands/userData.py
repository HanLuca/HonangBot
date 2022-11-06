import disnake, time, asyncio
from disnake.ext import commands

from .system._dataReceiver import DataReceiver
from .system._programReceiver import ProgramReceiver

#! List !#
userDataList = [ "1_Points", "2_Level", "3_Expoints", "4_Number", "5_JoinedTime" ]
coinDataList = [ "1COIN", "2COIN", "3COIN", "4COIN", "5COIN", "6COIN" ]
coinNameList = [ "1코인", "2코인", "3코인", "4코인", "5코인", "6코인" ]

class UserData(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name = "계정생성", description = "계정을 생성하고 Honang 봇을 즐겨보세요.")
    async def makeAccount(self, ctx):
        await ctx.response.defer(); await asyncio.sleep(3)

        if DataReceiver.check(ctx.author.id) == True: 
            await ctx.edit_original_response(embed = ProgramReceiver.embedError("\❓이미 계정이 존재합니다.", ctx.author))

        else:
            users = DataReceiver.get("SYSTEM", "1_UserAmount")

            #! Basic Datas !#
            listBasic = [
                {userDataList[0] : 1000}, {userDataList[1] : 1}, {userDataList[2] : 0},
                {userDataList[3] : users + 1}, {userDataList[4] : time.time()}
            ]
            for i in listBasic: DataReceiver.update(f"USERDATA/{ctx.author.id}", i)

            #! Coin Datas !#
            listCoin = [
                {"1_Amount" : 0}, {"2_PAmount" : 0}
            ]
            for i in range(0, len(coinDataList)):
                for a in listCoin:
                    DataReceiver.update(f"USERDATA/{ctx.author.id}/COIN/{coinDataList[i]}", a)

            #! System Datas !#
            DataReceiver.update("SYSTEM", {"1_UserAmount" : users + 1})

            embed = disnake.Embed (
                description = f"""
                {ctx.author.mention} 님의 계정이 새로 생성되었습니다.

                **┌────── [ 생성 정보 ] ──────┐**
                \🕐 <t:{round(time.time())}:R> 에 생성됨
                \😁 {users + 1} 번째 유저님

                """,
                color = 0x2f3136
            ); ProgramReceiver.embedFooter(embed, ctx.author)

            await ctx.edit_original_response(embed = embed)


    @commands.slash_command(name = "계정조회", description = "당신 또는 멤버의 계정을 조회하고 여러 정보를 확인해보세요!")
    async def seeAccount(self, ctx, member : disnake.Member = None):
        await ctx.response.defer(); await asyncio.sleep(3)

        if member == None: member = ctx.author
        if DataReceiver.check(member.id) == False:
            await ctx.edit_original_response(embed = ProgramReceiver.embedError(f"\❓{member.mention} 님의 계정이 존재하지 않습니다.\n**`/계정생성`** 명령어를 통해 가입해주세요.", member))
        
        else:
            #! Account Get !#
            userAccount = []
            for i in userDataList:
                userAccount.append(DataReceiver.get(f"USERDATA/{member.id}", i))

            embed = disnake.Embed (
                title = f"{member.name}'S PROFILE",
                description = f"""
                {member.mention} 님은 {userAccount[3]} 번째 유저에요!

                **┌────── [ 유저 정보 ] ──────┐**
                """,
                color = 0x2f3136
            ); ProgramReceiver.embedFooter(embed, ctx.author)
            embed.add_field("**\✨ Points**", f"**```{userAccount[0]} Cpt```**", inline = True)
            embed.add_field("**\💹 Level**", f"**```{userAccount[1]} Lv```**", inline = True)
            embed.add_field("**\❇️ Expoints**", f"**```{userAccount[2]} Exp```**", inline = False)

            embed.add_field("**\🕐 Join Time**", f"**<t:{round(userAccount[4])}>** ( **<t:{round(userAccount[4])}:R>** )", inline = False)

            try: embed.set_thumbnail(url = f"{member.avatar.url}")
            except: embed.set_thumbnail(url = "https://img1.daumcdn.net/thumb/C176x176/?fname=https://k.kakaocdn.net/dn/duEYdw/btq4wv9nziQ/M1IK8nqIuE9rlfFgjt3LQ0/img.png")

            await ctx.edit_original_response(embed = embed)