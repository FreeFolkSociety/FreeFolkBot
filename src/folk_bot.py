import logging
import os
import discord
from discord.ext import commands

logging.basicConfig(level=os.getenv("LOG_LEVEL", "DEBUG").upper())
log = logging.getLogger("FolkBot")


intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix='=', intents=intents)

bot.load_extension("cogs.voicefolk")

bot.run(os.environ['BOT_TOKEN'])
