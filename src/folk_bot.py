import logging
import os
import discord
import asyncio
from discord.ext import commands

logging.basicConfig(level=os.getenv("LOG_LEVEL", "DEBUG").upper())
log = logging.getLogger("FolkBot")


intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix='=', intents=intents)

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")
        # await bot.start(os.environ['BOT_TOKEN'])
bot.run(os.environ['BOT_TOKEN'])





    
        


