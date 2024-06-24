import discord
from discord.ext import commands
from discord import app_commands

import json
from llamaapi import LlamaAPI
import os


def build(message: str) -> dict:

    #Build the API request
    return {
        "messages": [
            {"role": "user", "content": message},
        ],
        "stream": False,
    }

# Execute the Request
#response = llama.run(api_request_json)
#print(json.dumps(response.json(), indent=2))



class Ai(commands.Cog):
    def __init__(self):
        # Initialize the SDK
        self.llama = LlamaAPI(os.getenv("LLAMA_API"))

    @app_commands.command(description="Задать вопрос LLAMA")
    @app_commands.describe(request="Ваш запрос тут")
    async def ai(self, interaction: discord.Interaction, request: str) -> None:
        await interaction.response.send_message("Загрузка...")
        response = self.llama.run(build(request))
        await interaction.edit_original_response(content=response)
