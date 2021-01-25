import discord
from discord.utils import get
import os

FreeFolk_Voice_ID = int(os.environ['VOICE_ROLE_ID'])


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_voice_state_update(self, member, before, after):
        #when someone joins
        if not before.channel and after.channel:
            role = get(member.guild.roles, id=FreeFolk_Voice_ID)
            await member.add_roles(role)

        #when someone leaves
        if before.channel and not after.channel:
            role = get(member.guild.roles, id=FreeFolk_Voice_ID)
            await member.remove_roles(role)

intents = discord.Intents.default()
intents.voice_states = True

client = MyClient(intents=intents)
client.run(os.environ['BOT_TOKEN'])