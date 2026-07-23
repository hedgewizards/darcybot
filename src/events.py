import interactions

from src import database


class Events(interactions.Extension):

    @interactions.listen()
    async def on_startup(self):
        print(f"Logged in as {self.bot.user}")

        for guild in self.bot.guilds:
            database.add_server(guild.id)


    @interactions.listen()
    async def on_guild_join(self, event):
        database.add_server(event.guild.id)