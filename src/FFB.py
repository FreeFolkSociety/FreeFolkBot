import discord
from discord.utils import get
import yaml
import os
import logging

FreeFolk_Voice_ID = int(os.environ['VOICE_ROLE_ID'])

with open("channel_to_role_mapping.yaml", 'r') as stream:
    try:
        settings = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


def set_up_logging():
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "DEBUG").upper())
    log = logging.getLogger("FolkBot")

    return log


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_voice_state_update(self, member, before, after):
        channel_mapping = settings['Voice_Cat_to_channel']
        LOGGER.debug(f"following data for event happend: \n "
                     f"User: {member} \n "
                     f"State Before: {before} \n "
                     f"State After:{after}")

        # when someone changes channel
        if not before.channel == after.channel:
            LOGGER.debug(f"detected channel change from {before.channel} to {after.channel}")
            if before.channel:
                LOGGER.debug(f"leaving channel {before.channel} so removing previous channel role")
                if before.channel.category.id in channel_mapping.keys():
                    channel = get(member.guild.channels, id=channel_mapping[before.channel.category.id])
                    LOGGER.info(f"User:{member} "
                                f"left voice channel: {before.channel}, "
                                f"In known catogory: {before.channel.category.name}, remove {channel} rights")
                    await channel.set_permissions(member, overwrite=None)
                else:
                    LOGGER.info(f"User:{member} "
                                f"left voice channel: {before.channel}, "
                                f"In unknown catogory: {before.channel.category.name}, cannot remove Rights")

            if after.channel:
                LOGGER.debug(f"joining channel {after.channel} so giving channel role")
                if after.channel.category.id in channel_mapping.keys():
                    channel = get(member.guild.channels, id=channel_mapping[after.channel.category.id])
                    LOGGER.info(f"User:{member} "
                                f"joined voice channel: {after.channel}, "
                                f"In known catogory: {after.channel.category.name}, giving {channel} rights")
                    overwrite = discord.PermissionOverwrite()
                    overwrite.send_messages = True
                    overwrite.add_reactions = True
                    overwrite.embed_links = True
                    overwrite.attach_files = True
                    await channel.set_permissions(member, overwrite=overwrite)
                else:
                    LOGGER.error(f"User:{member} "
                                 f"joined voice channel: {after.channel}, "
                                 f"In unknown catogory: {after.channel.category.name}, cannot give Rights")


intents = discord.Intents.default()
intents.voice_states = True

LOGGER = set_up_logging()

client = MyClient(intents=intents)
client.run(os.environ['BOT_TOKEN'])
