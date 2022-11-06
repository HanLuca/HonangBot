import disnake, time
from disnake.ext import commands

class ProgramReceiver():

    def embedFooter(embed, user):
        try: user.avatar.url
        except: avatar = "https://img1.daumcdn.net/thumb/C176x176/?fname=https://k.kakaocdn.net/dn/duEYdw/btq4wv9nziQ/M1IK8nqIuE9rlfFgjt3LQ0/img.png"
        else: avatar = user.avatar.url
        return embed.set_footer(text = f"{user.name}", icon_url = avatar)

    def embedError(message, user):
        embed = disnake.Embed (
            description = f"""
            {message}
            """,
            color = 0x2f3136

        ); ProgramReceiver.embedFooter(embed, user)
        return embed

    def embedLoading(user):
        embed = disnake.Embed (
            description = f"<a:loop:1036645734994419804> Loading ..",
            color = 0x2f3136,
        ); ProgramReceiver.embedFooter(embed, user)
        return embed

    def hostCheck(user : int):
        if not user == 869582271387148312: return False
        else: return True

    def log(event : str, index : str):
        with open("Log.txt", "a") as f:
            f.write(
f"""
[ {time.strftime('%c', time.localtime(time.time()))} ] -> {event}

{index}
=================================================================
"""
            )

    def notation(notation_ : int, num : int):
        resultNum = [num]; resultR = []
        loopNum = 0
        while True:
            if resultNum[loopNum] < notation_:
                resultR.append(int(str(resultNum[loopNum])[0:1]))
                break
            
            else:
                index = resultNum[loopNum] / notation_; resultNum.append(index)
                indexr = resultNum[loopNum] % notation_; resultR.append(int(str(indexr)[0:1]))
                loopNum += 1
                continue
                
        notationResult = f""
        for i in range(0, len(resultR)):
            notationResult += str(resultR[i])
        
        return notationResult