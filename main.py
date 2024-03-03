import logging
import discord
from discord.ext import commands
from config import TOKEN
import my_commands


class Bot(commands.Bot):
    handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="/", intents=intents)

    async def on_ready(self) -> None:
        print(f"We have logged in as {self.user} | {self.user.id}")
        await my_commands.setup(self)
        print(f"The commands has been initialized")

        await self.tree.sync()
        print(f"Commands tree has been sync")

        print(f"Number of guilds: {len(bot.guilds)}")


if __name__ == "__main__":
    bot = Bot()
    bot.run(TOKEN, log_handler=Bot.handler, log_level=logging.DEBUG)