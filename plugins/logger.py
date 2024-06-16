import discord
from discord.ext import commands

import config


def should_logged(message: discord.Message):
        if message.author.bot:
            return False
        if message.channel.id == config.CHANNEL_LOGS_ID:
            return False
        return True


async def copy_attachments(message: discord.Message) -> list[discord.Attachment] | None:
    if achts := message.attachments:
        files = []
        for file in achts:
            files.append(await file.to_file(use_cached=True))
        return files

    return None


class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logs_channel: discord.TextChannel = bot.get_channel(config.CHANNEL_LOGS_ID)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before: discord.Message, message_after: discord.Message) -> None:
        if not should_logged(message_after):
            return

        description = f"{message_before.content}\
            \nTo:\n{message_after.content}"
        embed = discord.Embed(description=description, color=discord.Color.yellow(), url=message_after.jump_url, title=message_after.channel.name)
        embed.set_author(name=message_after.author.name, icon_url=message_after.author.avatar)
        embed.set_footer(text="#edited")
        files = await copy_attachments(message_before)
        await self.logs_channel.send(embed=embed, files=files)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        if not should_logged(message):
            return

        embed = discord.Embed(description=message.content, color=discord.Color.red(), url=message.jump_url, title=message.channel.name)
        embed.set_author(name=message.author.name, icon_url=message.author.avatar)
        embed.set_footer(text="#deleted")
        files = await copy_attachments(message)
        await self.logs_channel.send(embed=embed, files=files)
