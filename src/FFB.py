import discord
from discord.utils import get
import os
import logging

FreeFolk_Voice_ID = int(os.environ['VOICE_ROLE_ID'])


def set_up_logging():
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "DEBUG").upper())
    log = logging.getLogger("FolkBot")

    return log


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_voice_state_update(self, member, before, after):
        LOGGER.debug(f"following data for event happend: \n "
                     f"User: {member} \n "
                     f"State Before: {before} \n "
                     f"State After:{after}")

        # when someone joins
        if not before.channel and after.channel:
            role = get(member.guild.roles, id=FreeFolk_Voice_ID)
            LOGGER.info(f"User:{member} joined voice channel: {after.channel} giving Role")
            await member.add_roles(role)

        # when someone leaves
        if before.channel and not after.channel:
            role = get(member.guild.roles, id=FreeFolk_Voice_ID)
            LOGGER.info(f"User:{member} left voice channel: {before.channel} removing Role")
            await member.remove_roles(role)


intents = discord.Intents.default()
intents.voice_states = True

LOGGER = set_up_logging()

client = MyClient(intents=intents)
client.run(os.environ['BOT_TOKEN'])
