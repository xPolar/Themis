# Imports
## Libraries included within Python
import asyncio
import datetime

## Libraries that must be installed with pip
import aiohttp, discord
from colorama import Fore, Back, Style, init
from discord.ext import commands

## Files on this machine
import config

# Initialize colorama
init(autoreset = True)

# Function to get the prefix whenever a message is sent
async def get_prefix(bot, message):
    if message.guild == None:
        return commands.when_mentioned_or(config.prefix)(bot, message)
    else:
        document = config.cluster["servers"]["prefixes"].find_one({"_id": message.guild.id})
        return commands.when_mentioned_or(document["prefix"])(bot, message) if document != None else commands.when_mentioned_or(config.prefix)(bot, message)

# Initiates the AutoShardedBot class, instead of having to deal with manually sharding discord.py will handle that for us.
bot = commands.AutoShardedBot(command_prefix = get_prefix, case_insensitive = True)

# All of the cogs within the bot that we want to load
cogs = []

# Loads all of our cogs
for cog in cogs:
    bot.load_extension(f"cogs.{cog}")
    print(f"{Style.BRIGHT}{Fore.GREEN}[SUCCESS]{Fore.WHITE} Loaded cogs.{cog}")

async def owner(ctx):
    return ctx.author.id in config.ownerids

@bot.command()
@commands.check(owner)
async def restart(ctx, cog = None):
    """
    Restart the bot's cogs.
    """
    print()
    for cog in cogs:
        bot.reload_extension(f"cogs.{cog}")
        print(f"{Style.BRIGHT}{Fore.GREEN}[SUCCESS]{Fore.WHITE} Reloaded cogs.{cog}")
    embed = discord.Embed(
        title = "Bot Restarted",
        description = "All cogs have been reloaded!",
        color = config.maincolor
    )
    await ctx.send(embed = embed)
    print(f"{Style.BRIGHT}{Fore.CYAN}[BOT-RESTARTED]{Fore.WHITE} Restart by {ctx.author} - {ctx.author.id}, I'm currently in {len(bot.guilds)} servers with {len(bot.users)} users!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.BadArgument):
        return
    elif isinstance(error, commands.CheckFailure):
        return
    elif isinstance(error, commands.BadUnionArgument):
        return
    else:
        try:
            embed = discord.Embed(
                    title = "Error",
                    description = f"**```\n{error}\n```**",
                    color = config.errorcolor
            )
            embed.set_footer(text = "Please report this to Polar#6880")
            await ctx.send(embed = embed)
        except:
            return
        raise error

@bot.event
async def on_guild_join(guild):
    embed = discord.Embed(
        title = "Joined a server!",
        timestamp = datetime.datetime.utcnow(),
        color = 0x77DD77
    )
    embed.add_field(name = "Server Name", value = guild.name)
    embed.add_field(name = "Server Members", value = len(guild.members))
    embed.add_field(name = "Server ID", value = guild.id)
    embed.add_field(name = "Server Owner", value = f"{guild.owner.name}#{guild.owner.discriminator}")
    embed.add_field(name = "Server Owner ID", value = guild.owner.id)
    embed.set_footer(text = f"I am now in {len(bot.guilds)} servers", icon_url = guild.icon_url)
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(config.webhook, adapter = discord.AsyncWebhookAdapter(session))
        await webhook.send(embed = embed, username = "Joined a server")

@bot.event
async def on_guild_remove(guild):
    embed = discord.Embed(
        title = "Left a server!",
        timestamp = datetime.datetime.utcnow(),
        color = 0xFF6961
    )
    embed.add_field(name = "Server Name", value = guild.name)
    embed.add_field(name = "Server Members", value = len(guild.members))
    embed.add_field(name = "Server ID", value = guild.id)
    embed.add_field(name = "Server Owner", value = f"{guild.owner.name}#{guild.owner.discriminator}")
    embed.add_field(name = "Server Owner ID", value = guild.owner.id)
    embed.set_footer(text = f"I am now in {len(bot.guilds)} servers", icon_url = guild.icon_url)
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(config.webhook, adapter = discord.AsyncWebhookAdapter(session))
        await webhook.send(embed = embed, username = "Left a server")

@bot.event
async def on_shard_ready(shard_id):
    print(f"{Style.BRIGHT}{Fore.CYAN}[SHARD-STARTED]{Fore.WHITE} Shard {Fore.YELLOW}{shard_id}{Fore.WHITE} has started!")

@bot.event
async def on_ready():
    print(f"{Style.BRIGHT}{Fore.CYAN}[BOT-STARTED]{Fore.WHITE} I'm currently in {len(bot.guilds)} servers with {len(bot.users)} users!")
    await bot.change_presence(status = discord.Status.dnd, activity = discord.Game(f"with {config.prefix}help"))

bot.run(config.token)