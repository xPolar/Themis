# Imports.
## Libraries that need to be installed through pip.
from colorama import Fore, Style
import discord
from discord.ext import commands

# Files on this machine.
import config

class MemberEvents(commands.Cog):
    
    def __init__ (self, bot):
        self.bot = bot

    # Event listener for whenever a member is updated.
    @commands.Cog.listener()
    async def on_member_update(self, before, after):

        # Reset a member's nickname if they are trying to hoist themselves.
        if before.bot == False and before.display_name != after.display_name:
            changed = False
            for char in ["!", "$", "%", "^", "&", "*", "(", ")", ",", ".", ">", "?"]:
                if after.display_name.startswith(char):
                    try:
                        await after.edit(nick = None)
                        changed = True
                    except discord.Forbidden:
                        print(f"{Style.BRIGHT}{Fore.RED}[MEMBER EVENTS]{Fore.WHITE} I don't have permissions to update the nickname of {after.id} in {after.guild} {after.guild.id}!")
                    break
            if changed == False:
                document = config.cluster["servers"]["badnames"].find_one({"_id": after.guild.id})
                if document != None:
                    for name in document["names"]:
                        if name.lower() in after.display_name.lower():
                            try:
                                await after.edit(nick = None)
                            except discord.Forbidden:
                                print(f"{Style.BRIGHT}{Fore.RED}[MEMBER EVENTS]{Fore.WHITE} I don't have permissions to update the nickname of {after.id} in {after.guild} {after.guild.id}!")
                            break
        
        # Ban a member if navis115 is in their name (Known Raider)
        if "navis115" in after.display_name:
            try:
                await after.ban(reason = "Known raider.")
            except discord.Forbidden:
                print(f"{Style.BRIGHT}{Fore.RED}[MEMBER EVENTS]{Fore.WHITE} I don't have permissions to ban navi115 in {after.guild} {after.guild.id}!")

    # Event listener for whenever a member joins.
    @commands.Cog.listener()
    async def on_member_join(self, member):
        
        # Ban a member if navis115 is in their name (Known Raider)
        if "navis115" in member.name or "navis115" in member.display_name:
            try:
                await member.ban(reason = "Known raider.")
            except discord.Forbidden:
                print(f"{Style.BRIGHT}{Fore.RED}[MEMBER EVENTS]{Fore.WHITE} I don't have permissions to ban navi115 in {member.guild} {member.guild.id}!")

def setup(bot):
    bot.add_cog(MemberEvents(bot))