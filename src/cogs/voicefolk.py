import discord
import yaml
from discord.ext import commands
from discord.utils import get
import logging


class VoiceFolk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("FolkBot")
        with open("channel_to_role_mapping.yaml", 'r') as stream:
            try:
                self.settings = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                self.logger.exception("exc")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        channel_mapping = self.settings['Voice_Cat_to_channel']
        self.logger.error("help im in a cog")
        self.logger.debug(f"following data for event happend: \n "
                     f"User: {member} \n "
                     f"State Before: {before} \n "
                     f"State After:{after}")

        # when someone changes channel
        if not before.channel == after.channel:
            rights_update = True
            if before.channel and after.channel:
                self.logger.debug("both channels defined")
                if before.channel.category == after.channel.category:
                    rights_update = False
                    self.logger.info(f"User:{member} "
                                f"switched channels: from: {before.channel} to: {after.channel}, "
                                f"In same catogory: {before.channel.category.name}, skipping rights assingment")

            self.logger.debug(f"detected channel change from {before.channel} to {after.channel}")
            if before.channel and rights_update:
                self.logger.debug(f"leaving channel {before.channel} so removing previous channel role")
                if before.channel.category.id in channel_mapping.keys():
                    channel = get(member.guild.channels, id=channel_mapping[before.channel.category.id])
                    self.logger.info(f"User:{member} "
                                f"left voice channel: {before.channel}, "
                                f"In known catogory: {before.channel.category.name}, remove {channel} rights")
                    await channel.set_permissions(member, overwrite=None)
                else:
                    self.logger.info(f"User:{member} "
                                f"left voice channel: {before.channel}, "
                                f"In unknown catogory: {before.channel.category.name}, cannot remove Rights")

            if after.channel and rights_update:
                self.logger.debug(f"joining channel {after.channel} so giving channel role")
                if after.channel.category.id in channel_mapping.keys():
                    channel = get(member.guild.channels, id=channel_mapping[after.channel.category.id])
                    self.logger.info(f"User:{member} "
                                f"joined voice channel: {after.channel}, "
                                f"In known catogory: {after.channel.category.name}, giving {channel} rights")
                    overwrite = discord.PermissionOverwrite()
                    overwrite.send_messages = True
                    overwrite.add_reactions = True
                    overwrite.embed_links = True
                    overwrite.attach_files = True
                    await channel.set_permissions(member, overwrite=overwrite)
                else:
                    self.logger.error(f"User:{member} "
                                 f"joined voice channel: {after.channel}, "
                                 f"In unknown catogory: {after.channel.category.name}, cannot give Rights")


def setup(bot):
    bot.add_cog(VoiceFolk(bot))
