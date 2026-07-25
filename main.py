import os

import interactions
from dotenv import load_dotenv

from src import database

load_dotenv()

token = os.getenv("DARCY_TOKEN")
debug_scope = os.getenv("DARCY_DEBUG_SCOPE")
intents = interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT

client_args = {
    "token": token,
    "intents": intents
}

if debug_scope:
    client_args["debug_scope"] = int(debug_scope)

bot = interactions.Client(**client_args)

database.initialize()

bot.load_extension("src.events")
bot.load_extension("src.commands")

bot.start()