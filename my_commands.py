import discord
from discord.ext import commands
from discord import app_commands
from gigachat import GigaChat

import config


class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Задать вопрос Gigachat")
    @app_commands.describe(request="Ваш запрос тут")
    async def ai(self, interaction: discord.Interaction, request: str) -> None:
        await interaction.response.send_message("Загрузка...")
        with GigaChat(
            credentials=config.GIGACHAT_TOKEN, verify_ssl_certs=False
        ) as giga:
            response = giga.chat(request)
            await interaction.edit_original_response(
                content=response.choices[0].message.content
            )

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before and before.channel:
            if (
                not before.channel.members
                and before.channel.category.id == TEMPORARY_CHANNELS_CATEGORY_ID
            ):
                await before.channel.delete()

        if after:
            if after.channel.id == CREATE_TEMPORARY_CHANNEL_ID:
                guild = after.channel.guild
                category = discord.utils.get(
                    guild.categories, id=TEMPORARY_CHANNELS_CATEGORY_ID
                )
                channel = await guild.create_voice_channel(
                    f"канал {member.display_name}", category=category
                )
                await member.move_to(channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MyCog(bot))
