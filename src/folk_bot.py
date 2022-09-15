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

async def main():
    async with bot:
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                await bot.load_extension(f"cogs.{file[:-3]}")
        await bot.load_extension('my_extension')
        await bot.start(os.environ['BOT_TOKEN'])
        #bot.run(os.environ['BOT_TOKEN'])





    
        


