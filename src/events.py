from src import database


def setup_events(bot, debug_mode):

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")

        for guild in bot.guilds:
            database.add_server(guild.id)
            if debug_mode:
                await bot.tree.sync(guild=guild)


        await bot.tree.sync()


    @bot.event
    async def on_guild_join(guild):
        database.add_server(guild.id)