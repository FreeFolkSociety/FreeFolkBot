import logging
import os
import discord
from discord.ext import commands

logging.basicConfig(level=os.getenv("LOG_LEVEL", "DEBUG").upper())
log = logging.getLogger("FolkBot")


intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix='=', intents=intents)

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        await bot.load_extension(f"cogs.{file[:-3]}")

bot.run(os.environ['BOT_TOKEN'])
