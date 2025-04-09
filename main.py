
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Create bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def load_extensions():
    await bot.load_extension("commands.ping")
    await bot.load_extension("commands.message")

@bot.event
async def on_ready():
    await load_extensions()
    # Synchronisiere Commands global
    await bot.tree.sync()
    print(f'{bot.user} has connected to Discord!')

bot.run(TOKEN)
