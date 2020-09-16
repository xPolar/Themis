# Imports
## Libraries that must be installed with pip
from colorama import Style, Fore
import discord, time
from discord.ext import commands
## Files on this machine
import config

class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases = ["latency"])
    async def ping(self, ctx):
        """
        View the host and bot latency.
        """
        t1 = time.perf_counter()
        await ctx.trigger_typing()
        t2 = time.perf_counter()
        embed = discord.Embed(
            title = "🏓 Pong!",
            description = f"Host latency is { round((t2 - t1) * 1000) }ms\nAPI latency is { int(round(self.bot.latency * 1000, 2)) }ms",
            color = config.maincolor
        )
        if (round((t2 - t1) * 1000) > 500) or (round(self.bot.latency * 1000, 2) > 500):
            print(f"{Style.BRIGHT}{Fore.RED}[WARNING]{Fore.WHITE} API latency is { round((t2 - t1) * 1000) }ms & host latency is { int(round(self.bot.latency * 1000, 2)) }ms")
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Ping(bot))