# Imports.
## Libraries default to Python.
import asyncio

## Libraries that need to be installed through pip.
from colorama import Fore, Style
import discord
from discord.ext import commands

# Files on this machine.
import config

class MessageEvents(commands.Cog):
    
    def __init__ (self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        
        # Make sure the message isn't in a DM or by a bot.
        if message.guild != None and message.bot == False:

            # Ban member if the message they send has navis115 in it
            if "navis115" in message.content:
                await message.author.ban(reason = "Known Raider")
                return

            # If the message is from SSBU.
            if message.guild.id == 433257889457635329:

                # Autorole Channel.
                if message.channel.id == 705825733066358825:
                    heros = message.content.split(",")
                    given = 0 # They can't get more then 5 roles at a time so we put an integer in place to have one added each role added.
                    for hero in heros:
                        if given <= 4:
                            hero = hero[1:] if hero.startswith(" ") else hero
                            name = " ".join([ word.lower().title() for word in hero.split(" ") ])
                            role = discord.utils.get(message.guild.roles, name)
                            if role != None and role.name in ["Hero", "Mario", "Donkey Kong", "Link", "Samus", "Dark Samus", "Yoshi", "Kirby", "Pikachu", "Luigi", "Ness", "Captain Falcon", "Jigglypuff", "Peach", "Daisy", "Bowser", "Ice Climbers", "Sheik", "Zelda", "Dr Mario", "Pichu", "Falco", "Marth", "Lucina", "Young Link", "Ganondorf", "Mewtwo", "Roy", "Chrom", "Mr Game And Watch", "Meta Knight", "Pit", "Dark Pit", "Zero Suit Samus", "Wario", "Snake", "Ike", "Pkmn Trainer", "Diddy Kong", "Lucas", "Sonic", "King Dedede", "Olimar", "Lucario", "ROB", "Toon Link", "Wolf", "Villager", "Mega Man", "Wii Fit Trainer", "Rosalina And Luma", "Little Mac", "Greninja", "Mii Fit Brawler", "Mii Fit Swordfighter", "Mii Gunner", "Palutena", "Pac Man", "Robin", "Shulk", "Bowser Jr", "Duck Hunt", "Ryu", "Ken", "Cloud", "Corrin", "Bayonetta", "Inkling", "Ridley", "Simon", "Random", "Richter", "King K Rool", "Isabelle", "Incineroar", "Piranha Plant", "Joker", "Banjo And Kazooie", "Terry", "Byleth", "Game & Watch", "Min Min", "Fox", "Asia", "Europe", "Na Central", "Na East", "Na West", "Oceania", "South America"]:
                                await message.author.add_roles(role) if role not in message.author.roles else await message.author.remove_roles(role)
                    try:
                        await message.delete()
                    except discord.NotFound:
                        pass

                # Moderator Ping.
                if "@moderator" in message.content.lower() or  "<@&516276897617936385>" in message.content:
                    permissions = message.channel.permissions_for(message.author)
                    if permissions.mention_everyone == False:
                        embed = discord.Embed(
                            title = "A Vote Has Started",
                            description = f"{message.author.mention} has tried to mention <@&516276897617936385>, there will now be a vote to ping the mods or not! This vote will end in 120 seconds.",
                            color = config.maincolor
                        )
                        vote = await message.channel.send(embed = embed)
                        def check(reaction, user):
                            return reaction.message.id == vote.id and str(reaction.emoji) == "✅"
                        try:
                            await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
                        except asyncio.TimeoutError:
                            await message.delete()
                        else:
                            try:
                                await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
                            except asyncio.TimeoutError:
                                await message.delete()
                            else:
                                try:
                                    await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
                                except asyncio.TimeoutError:
                                    await message.delete()
                                else:
                                    await message.delete()
                                    await message.channel.send(f"{message.author.mention} has pinged <@&516276897617936385>!")

def setup(bot):
    bot.add_cog(MessageEvents(bot))