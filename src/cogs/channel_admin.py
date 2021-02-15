import discord
from discord.ext import commands
from discord.utils import get
import logging


class ChannelAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("FolkBot.ChannelAdmin")

    @commands.command()
    @commands.is_owner()
    async def checknsfw(self, ctx):
        not_correct_channels = []
        for channel in ctx.guild.text_channels:
            self.logger.debug(f"found channel: {channel}")
            if not channel.is_nsfw():
                not_correct_channels.append(channel)

        self.logger.debug(f"list is: {not_correct_channels}")
        if len(not_correct_channels) == 0:
            ctx.send("no channels found that are not NSFW")
        else:
            text_list = []
            text_list.append("the following Channels are not NSFW")
            self.logger.debug("creating list")
            for channel in not_correct_channels:
                text_list.append(f"{channel.category} {channel}")
            await ctx.send("\n".join(text_list))

    @commands.Cog.listener(name="on_guild_channel_create")
    async def make_channel_nsfw(self, channel):
        if "ticket-" in channel.name:
            await channel.edit(reason="Ticket created marked as NSFW", nsfw=True)


def setup(bot):
    bot.add_cog(ChannelAdmin(bot))
