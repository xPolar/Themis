# Imports
## Libraries that need to be installed through pip.
from colorama import Fore, Style
import discord
from discord.ext import commands

# Files on this machine.
import config

class Hoist(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def unhoist(self, ctx):
        """
        Dehoist all people who are trying to hoist themselves.
        """
        total = 0
        for member in ctx.guild.members:
            for char in ["!", "$", "%", "^", "&", "*", "(", ")", ",", ".", ">", "?"]:
                if member.display_name.startswith(char):
                    try:
                        await member.edit(nick = None)
                        total += 1
                    except discord.Forbidden:
                        print(f"{Style.BRIGHT}{Fore.RED}[HOIST]{Fore.WHITE} I don't have permissions to update the nickname of {member.id} in {ctx.guild} {ctx.guild.id}!")
        if total > 0:
            embed = discord.Embed(
                title = "No Members Unhoisted",
                description = "No one was unhoisted!",
                color = config.maincolor
            )
        else:
            embed = discord.Embed(
                title = "Members Unhoisted",
                description = f"I have unhoisted {total} member{ 's' if total > 1 else '' }!",
                color = config.maincolor
            )
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Hoist(bot))