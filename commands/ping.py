
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="ping", description="Antwortet mit pong")
    async def ping(self, ctx):
        await ctx.send("pong")

async def setup(bot):
    await bot.add_cog(Ping(bot))
