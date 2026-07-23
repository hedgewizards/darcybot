import os

import interactions
from dotenv import load_dotenv

from src import database

load_dotenv()

token = os.getenv("DARCY_TOKEN")
debug_scope = os.getenv("DARCY_DEBUG_SCOPE")
intents = interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT

bot = interactions.Client(
    token=token,
    debug_scope=int(debug_scope) if debug_scope else None,
    intents=intents
)

database.initialize()

bot.load_extension("src.events")
bot.load_extension("src.commands")

bot.start()