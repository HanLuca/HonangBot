import disnake, time
from disnake.ext import commands

from ._programReceiver import ProgramReceiver

class Embeds():

    def embedBetting_Success(user, coin, userCoin, expoint, expoints, level):
        embedIndex = f"""
        **\✅ {user.mention} 님이 도박에 성공하셨습니다!**

        **┌────── [ 도박 정보 ] ──────┐**
        \✅ 성공
        \✳️ + {expoint} Expoint ( {expoints} / {level * 1000} )
        \✨ + {2 * coin} Cpt **( 보유 : {userCoin} Cpt )**
        
        """
        return embedIndex

    def embedBetting_Fail(user, coin, userCoin):
        embedIndex = f"""
            **\😓 {user.mention} 님이 도박에 실패하셨습니다!**

            **┌────── [ 도박 정보 ] ──────┐**
            \😓 실패
            \✨ - {coin} Cpt **( 남은 돈 : {userCoin} Cpt )**
        """
        return embedIndex