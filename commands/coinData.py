import disnake, time, asyncio, random
from disnake.ext import commands, tasks

from .system._dataReceiver import DataReceiver
from .system._programReceiver import ProgramReceiver

from .userData import userDataList, coinDataList, coinNameList

class CoinData(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.coinChange.start()
    
    #! Owner Command !#
    @commands.command(name = "@host:coinSet")
    async def hostCoinSet(self, ctx):
        if ProgramReceiver.hostCheck(ctx.author.id) == True:
            mainCoinPath = f"SYSTEM/COIN"
            listCoin = [
                {"1_Price" : 1000}, {"2_BPrice" : 1000}, {"3_SellAmount" : 0}
            ]

            for i in range(0, len(coinDataList)):
                for a in listCoin:
                    DataReceiver.update(f"{mainCoinPath}/{coinDataList[i]}", a)
                    await ctx.send(f"Success : {coinDataList[i]} ( {a} )")

            ProgramReceiver.log("@host:coinSet", "코인 정보 초기화")

    @commands.command(name = "@host:coinUpdate")
    async def hostCoinUpdate(self, ctx):
        if ProgramReceiver.hostCheck(ctx.author.id) == True:
            self.stockChange.cancel(); await ctx.send("<-- Stop Loop -->")
            self.stockChange.start(); await ctx.send("<-- Start Loop -->")

            ProgramReceiver.log("@host:coinUpdate", "코인 가격 루프 재실행")

    #! Loop !#
    @tasks.loop(seconds = 60)
    async def coinChange(self):
        #! Variables !#
        mainStockPath = f"SYSTEM/COIN"
        
        for i in coinDataList:
            Price = DataReceiver.get(f"{mainStockPath}/{i}", "1_Price")
            BPrice = DataReceiver.get(f"{mainStockPath}/{i}", "2_BPrice")
            SellAmount = DataReceiver.get(f"{mainStockPath}/{i}", "3_SellAmount")
            
            if Price <= 0:
                ProgramReceiver.log(f"Coin Loop : {i}", "<= 0 -> FAIL")
                newPrice = random.randrange(0, 100)

                DataReceiver.update(f"{mainStockPath}/{i}", {"1_Price" : Price + newPrice})
                DataReceiver.update(f"{mainStockPath}/{i}", {"2_BPrice" : Price})

            else:
                newPrice = random.randrange(-100, 100)

                DataReceiver.update(f"{mainStockPath}/{i}", {"1_Price" : Price + newPrice})
                DataReceiver.update(f"{mainStockPath}/{i}", {"2_BPrice" : Price})

        ProgramReceiver.log(f"Coin Loop", f"All Success")

    #! Command !#
    @commands.slash_command(name = "코인", description = "코인 기능을 확인해보세요!")
    async def stock(self, ctx):
        pass

    @stock.sub_command(name = "정보", description = "코인 가격을 확인해보세요!")
    async def stockInfo(self, ctx):
        await ctx.response.defer(); await asyncio.sleep(1)

        if DataReceiver.check(ctx.author.id) == False:
            await ctx.edit_original_response(embed = ProgramReceiver.embedError(f"\❓{ctx.author.mention} 님의 계정이 존재하지 않습니다.\n**`/계정생성`** 명령어를 통해 가입해주세요.", ctx.author))

        else:
            #! Variables !#
            mainCoinPath = f"SYSTEM/COIN"
            mainPath = f"USERDATA/{ctx.author.id}"

            embed = disnake.Embed(color = 0x2f3136)
            for i in range(0, len(coinDataList)):
                #! Variables !#
                Price = DataReceiver.get(f"{mainCoinPath}/{coinDataList[i]}", "1_Price")
                BPrice = DataReceiver.get(f"{mainCoinPath}/{coinDataList[i]}", "2_BPrice")
                Amount = DataReceiver.get(f'{mainPath}/COIN/{coinDataList[i]}', '1_Amount')

                if Price - BPrice > 0: 
                    embed.add_field(f"{coinNameList[i]} ( {Amount} 주 )", f"```ansi\n[0;32m឵ {Price} Cpt ( ▲ {str(Price - BPrice)} )```", inline = True)

                elif Price - BPrice == 0: 
                    embed.add_field(f"{coinNameList[i]} ( {Amount} 주 )", f"```ansi\n[0;33m឵ {Price} Cpt ( ■ 0 )```", inline = True)

                else: 
                    embed.add_field(f"{coinNameList[i]} ( {Amount} 주 )", f"```ansi\n[0;31m឵ {Price} Cpt ( ▼ {str(Price - BPrice)[1:]} )```", inline = True)

        ProgramReceiver.embedFooter(embed, ctx.author)
        await ctx.edit_original_response(embed = embed)


    @stock.sub_command(name = "구매", description = "코인을 구매해서 대박을 노려보세요!")
    async def stockInfo(
        self, ctx, 
        coin : str = commands.Param(
            name = "coin", choices = [coinNameList[i] for i in range(0, len(coinNameList))]
        ),
        amount : int = 1
    ):
        await ctx.response.defer(); await asyncio.sleep(1)

        if DataReceiver.check(ctx.author.id) == False:
            await ctx.edit_original_response(embed = ProgramReceiver.embedError(f"\❓{ctx.author.mention} 님의 계정이 존재하지 않습니다.\n**`/계정생성`** 명령어를 통해 가입해주세요.", ctx.author))

        else:
            #! Variables !#
            mainCoinPath = f"SYSTEM/COIN"
            mainUserPath = f"USERDATA/{ctx.author.id}"

            locationCoin = coinNameList.index(coin)
            userCpt = DataReceiver.get(f"{mainUserPath}", "1_Points")

            if DataReceiver.get(f"{mainCoinPath}/{coinDataList[locationCoin]}", "1_Price") * amount > userCpt:
                await ctx.edit_original_response(embed = ProgramReceiver.embedError(f"\❓감당할 수 없는 가격입니다.", ctx.author))

            else:
                #! Variables !#
                coinAmount = DataReceiver.get(f"{mainUserPath}/COIN/{coinDataList[locationCoin]}", "1_Amount")
                priceAmount = DataReceiver.get(f"{mainUserPath}/COIN/{coinDataList[locationCoin]}", "2_PAmount")

                coinPrice = DataReceiver.get(f"{mainCoinPath}/{coinDataList[locationCoin]}", "1_Price")
                coinSells = DataReceiver.get(f"{mainCoinPath}/{coinDataList[locationCoin]}", "3_SellAmount")

                DataReceiver.update(f"{mainUserPath}", {"1_Points" : int(userCpt - (coinPrice * amount))})
                DataReceiver.update(f"{mainUserPath}/COIN/{coinDataList[locationCoin]}", {"1_Amount" : int(coinAmount + amount)})
                DataReceiver.update(f"{mainUserPath}/COIN/{coinDataList[locationCoin]}", {"2_PAmount" : int(priceAmount + (coinPrice * amount))})

                DataReceiver.update(f"{mainCoinPath}/{coinDataList[locationCoin]}", {"3_SellAmount" : int(coinSells + amount)})

                embed = disnake.Embed (
                    description = f"""
                    **\✅ {ctx.author.mention} 코인 구매가 완료되었습니다!**

                    **┌────── [ 구매 정보 ] ──────┐**
                    \📈 종목 : {coinNameList[locationCoin]} **( 가격 : {coinPrice}  Cpt )**
                    \📉 수량 : {amount} 개 **( 보유 : {coinAmount + amount} 개 )**
                    \✨ - {coinPrice * amount} Cpt **( 보유 : {userCpt - (coinPrice * amount)} Cpt )**
                    """,
                    color = 0x2f3136
                ); ProgramReceiver.embedFooter(embed, ctx.author)
                await ctx.edit_original_response(embed = embed)


    @stock.sub_command(name = "판매", description = "코인을 판매해서 수익을 얻어보세요!")
    async def stockInfo(
        self, ctx, 
        coin : str = commands.Param(
            name = "coin", choices = [coinNameList[i] for i in range(0, len(coinNameList))]
        ),
        amount : int = 1
    ):
        await ctx.response.defer(); await asyncio.sleep(1)

        if DataReceiver.check(ctx.author.id) == False:
            await ctx.edit_original_response(embed = ProgramReceiver.embedError(f"\❓{ctx.author.mention} 님의 계정이 존재하지 않습니다.\n**`/계정생성`** 명령어를 통해 가입해주세요.", ctx.author))

        else:
            #! Variables !#
            mainCoinPath = f"SYSTEM/COIN"
            mainUserPath = f"USERDATA/{ctx.author.id}"

            locationCoin = coinNameList.index(coin)
            userCpt = DataReceiver.get(f"{mainUserPath}", "1_Points")
            coinAmount = DataReceiver.get(f"{mainUserPath}/COIN/{coinDataList[locationCoin]}", "1_Amount")

            if coinAmount < amount:
                await ctx.edit_original_response(embed = ProgramReceiver.embedError(f"\❓감당할 수 없는 수량입니다.", ctx.author))

            else:
                coinPrice = DataReceiver.get(f"{mainCoinPath}/{coinDataList[locationCoin]}", "1_Price")
                coinSells = DataReceiver.get(f"{mainCoinPath}/{coinDataList[locationCoin]}", "3_SellAmount")

                DataReceiver.update(f"{mainUserPath}", {"1_Points" : int(userCpt + (coinPrice * amount))})
                DataReceiver.update(f"{mainUserPath}/COIN/{coinDataList[locationCoin]}", {"1_Amount" : int(coinAmount - amount)})

                DataReceiver.update(f"{mainCoinPath}/{coinDataList[locationCoin]}", {"3_SellAmount" : int(coinSells - amount)})

                embed = disnake.Embed (
                    description = f"""
                    **\✅ {ctx.author.mention} 코인 판매가 완료되었습니다!**

                    **┌────── [ 판매 정보 ] ──────┐**
                    \📈 종목 : {coinNameList[locationCoin]} **( 가격 : {coinPrice}  Cpt )**
                    \📉 수량 : {amount} 개 **( 보유 : {coinAmount - amount} 개 )**
                    \✨ + {coinPrice * amount} Cpt **( 보유 : {userCpt + (coinPrice * amount)} Cpt )**
                    """,
                    color = 0x2f3136
                ); ProgramReceiver.embedFooter(embed, ctx.author)
                await ctx.edit_original_response(embed = embed)