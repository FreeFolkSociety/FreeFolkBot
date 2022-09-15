import logging
import os
import discord
import asyncio
from discord.ext import commands

logging.basicConfig(level=os.getenv("LOG_LEVEL", "DEBUG").upper())
log = logging.getLogger("FolkBot")


intents = discord.Intents.default()
intents.voice_states = True

client = commands.Bot(command_prefix='=', intents=intents)

async def load_extensions():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            # cut off the .py from the file name
            await client.load_extension(f"cogs.{file[:-3]}")

async def main():
    async with client:
        await load_extensions()
        await client.start(os.environ['BOT_TOKEN'])

asyncio.run(main())

# for file in os.listdir("./cogs"):
#     if file.endswith(".py"):
#         bot.load_extension(f"cogs.{file[:-3]}")

# bot.run(os.environ['BOT_TOKEN'])





    
        


