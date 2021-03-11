import discord
from discord.ext import commands
from discord.utils import get
import logging
import yaml


class ChannelAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("FolkBot.ChannelAdmin")
        with open("channel_to_role_mapping.yaml", 'r') as stream:
            try:
                tmp_settings = yaml.safe_load(stream)
                self.settings = tmp_settings['ChannelAdmin']
            except yaml.YAMLError as exc:
                self.logger.exception(exc)
            except KeyError as exc:
                self.logger.exception(exc)

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

    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, *args):
        text = " ".join(args)
        log_channel = self.bot.get_channel(self.settings.get("bot_log_channel", ctx.channel))
        support_role = ctx.guild.get_role(self.settings["support_role"])
        muted_voice_category = discord.utils.get(ctx.guild.categories, id=self.settings["muted_voice_category"])
        member_role = ctx.guild.get_role(self.settings["user_role"])
        embed = discord.Embed(colour=discord.Colour(0xd0021b),
                              description=f"**Offender:** {member} \n "
                                          f"**Reason**: {text} \n "
                                          f"**Responsible moderator**: {ctx.author}",
                              type="rich")
        embed.set_author(name="Muted user", icon_url="https://cdn.discordapp.com/emojis/795751312292970516.png?v=1")
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False,
                                                               connect=False),
            member: discord.PermissionOverwrite(view_channel=True,
                                                speak=True,
                                                stream=True,
                                                connect=True,
                                                use_voice_activation=True),
            support_role: discord.PermissionOverwrite(view_channel=True,
                                                      speak=True,
                                                      stream=True,
                                                      connect=True,
                                                      use_voice_activation=True,
                                                      priority_speaker=True,
                                                      mute_members=True,
                                                      deafen_members=True,
                                                      move_members=True)
        }
        await ctx.guild.create_voice_channel(f"muted-{member.name}",
                                             overwrites=overwrites,
                                             category=muted_voice_category,
                                             reason=f"{member.name} is muted by {ctx.author}")
        #send embed to log channel
        await member.remove_roles(member_role,  reason=f"user is muted by {ctx.author}")
        await log_channel.send(embed=embed)

    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member, *args):
        member_role = ctx.guild.get_role(self.settings["user_role"])
        text = " ".join(args)
        voice_channel = discord.utils.get(ctx.guild.channels, name=f"muted-{member.name}")
        await voice_channel.delete()
        embed = discord.Embed(colour=discord.Colour.green(),
                              description=f"**Who:** {member} \n "
                                          f"**Reason**: {text} \n "
                                          f"**Responsible moderator**: {ctx.author}",
                              type="rich")
        embed.set_author(name="Unmuted user",
                         icon_url="https://github.com/twitter/twemoji/raw/master/assets/72x72/1f508.png")
        log_channel = self.bot.get_channel(self.settings.get("bot_log_channel", ctx.channel))
        await member.add_roles(member_role,  reason=f"user is unmuted by {ctx.author}")
        await log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(ChannelAdmin(bot))
