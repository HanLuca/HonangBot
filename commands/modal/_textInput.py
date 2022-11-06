import disnake, time, asyncio
from disnake.ext import commands
from disnake import TextInputStyle

from ..system._programReceiver import ProgramReceiver

#! ErrorNotice / 오류제보 !#
class ErrorNotice(disnake.ui.Modal):

    def __init__(self, bot):
        self.bot = bot

        components = [
            disnake.ui.TextInput (
                label = "제목 : 오류의 내용",
                placeholder = "오류의 내용을 간단하게 작성해주세요.",
                custom_id = "제목 : 오류의 내용",
                style = TextInputStyle.short,
                max_length = 100,
            ),
            disnake.ui.TextInput (
                label = "내용 : 오류에 관련한 구체적 사실 ( 발생 원인, 발생 상황 등 )",
                placeholder = "오류의 구체적 사실을 작성해주세요.",
                custom_id = "내용 : 오류에 관련한 구체적 사실 ( 발생 원인, 발생 상황 등 )",
                style = TextInputStyle.paragraph
            )
        ]
        super().__init__ (
            title = "오류 제보",
            custom_id = "errorNotice",
            components = components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        errorState = False
        embed = disnake.Embed(description = f"**\✅ 오류 제보됨 ( <t:{round(time.time())}> : <t:{round(time.time())}:R> )**", color = 0x2f3136)
        for key, value in inter.text_values.items():
            if "`" in value[:1024]: 
                errorState = True; break

            else:
                embed.add_field (
                    name = key.capitalize(),
                    value = f"```{value[:1024]}```",
                    inline = False
                )
        
        if errorState == True:
            embed = disnake.Embed(description = f"**\❎ 오류 제보 취소됨 ( <t:{round(time.time())}> : <t:{round(time.time())}:R> )**\n\n포함할 수 없는 기호가 들어갔습니다.", color = 0x2f3136)
            await inter.response.send_message(embed = embed, ephemeral = True)

        else:
            ProgramReceiver.embedFooter(embed, inter.author)
            await inter.response.send_message(embed = embed, ephemeral = True)

            admin = await self.bot.fetch_user("869582271387148312")
            await admin.send(embed = embed)