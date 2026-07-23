import discord
import os

intents = discord.Intents.default()
token = os.getenv("DARCY_TOKEN")

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

client.run(token)