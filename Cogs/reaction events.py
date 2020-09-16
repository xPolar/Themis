# Imports
## Libraries that must be installed with pip
from colorama import Style, Fore
import discord, time
from discord.ext import commands
## Files on this machine
import config

class ReactionEvents(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.guild_id != None:

            # Make sure the reaction isn't by a bot, is in the r/SmashBrosUltimate server, and the reaction is the observer reaction.
            if payload.member.bot == False and payload.guild_id == 433257889457635329 and payload.emoji.id == 736852733457465384:
                if 736850415248998430 in [ role.id for role in payload.member.roles ]:
                    channel = discord.utils.get(payload.member.guild.text_channels, id = 713802230964158576)
                    ctx_channel = discord.utils.get(payload.member.guild.text_channels, id = payload.channel_id)
                    if channel != None and ctx_channel != None:
                        try:
                            message = await ctx_channel.fetch_message(payload.message_id)
                        except discord.NotFound:
                            return
                        else:
                            await message.remove_reaction(payload.emoji, payload.member)
                            file = None
                            embed = discord.Embed(
                                title = "Agent Report",
                                color = config.maincolor
                            )
                            if message.content != "":
                                embed.description = message.content
                            if message.attachments != []:
                                file = await message.attachments[0].to_file()
                                embed.set_image(url = f"attachment://{file.filename}")
                            embed.add_field(name = "Extra Details", value = f"[Jump To Message]({message.jump_url})\nUser Mention: {message.author.mention}")
                            embed.set_author(name = f"Reported by {payload.member} in #{message.channel}", icon_url = payload.member.avatar_url)
                            embed.set_footer(text = f"Offender: {message.author} ID: {message.author.id}", icon_url = message.author.avatar_url)
                            if file == None:
                                await channel.send(embed = embed)
                            else:
                                await channel.send(file = file, embed = embed)


def setup(bot):
    bot.add_cog(ReactionEvents(bot))