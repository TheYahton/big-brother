import discord
from discord.ext import commands
from discord import app_commands
from gigachat import GigaChat

import config
import json
import os


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Задать вопрос Gigachat")
    @app_commands.describe(request="Ваш запрос тут")
    async def ai(self, interaction: discord.Interaction, request: str) -> None:
        if config.GIGACHAT_TOKEN:
            await interaction.response.send_message("Загрузка...")
            with GigaChat(
                credentials=config.GIGACHAT_TOKEN, verify_ssl_certs=False
            ) as giga:
                response = giga.chat(request)
                await interaction.edit_original_response(
                    content=response.choices[0].message.content
                )
        else:
            await interaction.response.send_message("Создатель бота жмот, который не удосужился дать мне API ключ :/")
    


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return


class VoiceMaster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temporary_channels = []
        self.data_load()
    
    def data_load(self):
        if os.path.exists('data/channels.json'):
            with open("data/channels.json", 'r') as data:
                self.temporary_channels = json.load(data)
    
    def data_save(self):
        with open("data/channels.json", "w") as outfile:
            json.dump(self.temporary_channels, outfile)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.channel:
            if (
                not before.channel.members
                and before.channel.id in self.temporary_channels
            ):
                self.temporary_channels.remove(before.channel.id)
                await before.channel.delete()
                self.data_save()

        if after.channel:
            if after.channel.id == config.CHANNEL_CREATOR_ID:
                guild: discord.Guild = after.channel.guild
                category = discord.utils.get(after.channel.guild.channels, id=config.CHANNEL_CREATOR_ID)
                channel = await guild.create_voice_channel(
                    f"канал {member.display_name}", category=category.category if category else None
                )
                await member.move_to(channel)
                self.temporary_channels.append(channel.id)
                self.data_save()

                await channel.set_permissions(member, manage_channels=True, mute_members=True, move_members=True, manage_roles=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))
    await bot.add_cog(VoiceMaster(bot))

