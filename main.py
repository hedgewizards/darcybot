import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv

from src import database
from src.commands import setup_commands
from src.events import setup_events

load_dotenv()

intents = discord.Intents.default()
token = os.getenv("DARCY_TOKEN")
use_debug = os.getenv("DARCY_DEBUG").lower() == "true"

client = discord.Client(intents=intents)

bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    intents=intents
)

database.initialize()

setup_commands(bot)
setup_events(bot, use_debug)

bot.run(token)