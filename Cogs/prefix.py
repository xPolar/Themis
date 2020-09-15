# Imports.
## Libraries that need to be installed through pip.
from colorama import Fore, Style
import discord
from discord.ext import commands

# Files on this machine.
import config

class Prefix(commands.Cog):
    
    def __init__ (self, bot):
        self.bot = bot
    
    @commands.group()
    async def prefix(self, ctx):
        if ctx.invoked_subcommand is None:
            prefix = config.cluster["servers"]["prefixes"].find_one({"_id": ctx.guild.id}) if ctx.guild != None else config.prefix
            embed = discord.Embed(
                description = f"Hey there, my name is {self.bot.display_name} and my prefix is `{ prefix['prefix'] if prefix != None else config.prefix }`!",
                color = config.maincolor
            )
            await ctx.send(embed = embed)
    
    @prefix.command()
    @commands.has_permissions(manage_guild = True)
    async def set(self, ctx, new_prefix = None):
        """
        Set the new prefix of the bot.
        """
        if new_prefix == None:
            embed = discord.Embed(
                title = "Empty Argument",
                description = f"Please provide a prefix to change to!",
                color = config.errorcolor
            )
        else:
            embed = discord.Embed(
                title = "Prefix Set",
                description = f"You have set {ctx.guild.name}'s prefix to `{new_prefix}`",
                color = config.maincolor
            )
            config.cluster["servers"]["prefixes"].update_one({"_id": ctx.guild.id}, {"$set": {"prefix": new_prefix}}, upsert = True)
        await ctx.send(embed = embed)

    @set.error
    async def set_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You require the **Manage Server** permission for this server!",
                color = config.errorcolor
            )
            await ctx.send(embed = embed)

    @prefix.command()
    @commands.has_permissions(manage_guild = True)
    async def reset(self, ctx):
        """
        Reset the prefix of the bot to it's default.
        """
        embed = discord.Embed(
            title = "Prefix Reset",
            description = f"You have reset {ctx.guild.name}'s prefix to `{config.prefix}`",
            color = config.maincolor
        )
        config.errorcolor["servers"]["prefixes"].delete_one({"_id": ctx.guild.id})
        await ctx.send(embed = embed)

    @reset.error
    async def reset_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You require the **Manage Server** permission for this server!",
                color = config.errorcolor
            )
            await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Prefix(bot))