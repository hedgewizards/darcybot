import interactions
from interactions.api import events
from src.highlights import process_positive_vote, process_any_vote

from src import database
from src import leaderboard

class Events(interactions.Extension):

    @interactions.listen(events.Startup)
    async def on_startup(self):
        print(f"Logged in as {self.bot.user}")

        for guild in self.bot.guilds:
            database.add_server(guild.id)


    @interactions.listen(events.GuildJoin)
    async def on_guild_join(self, event):
        database.add_server(event.guild.id)

    @interactions.listen(events.MessageReactionAdd)
    async def on_reaction_add(self, event):
        guild_settings = database.get_server(event.message.guild.id)

        if guild_settings is None:
            return

        received_emote = str(event.emoji)
        positive_emote = guild_settings["vote_positive_emote"]
        negative_emote = guild_settings["vote_negative_emote"]

        if received_emote == positive_emote:
            database.add_vote(
                event.message.guild.id,
                event.message.id,
                event.message.author.id,
                event.author.id,
                1
            )

            await process_positive_vote(self.bot, event.message, guild_settings)

            leaderboard.trigger_update_leaderboard(
                self.bot,
                event.message.guild
            )

            print(
                f"Positive vote: message={event.message.id}, "
                f"voter={event.author.id}, "
                f"emote={received_emote}, "
                f"configured_positive={positive_emote}"
            )

        elif received_emote == negative_emote:
            database.add_vote(
                event.message.guild.id,
                event.message.id,
                event.message.author.id,
                event.author.id,
                -1
            )

            await process_any_vote(self.bot, event.message, guild_settings)

            leaderboard.trigger_update_leaderboard(
                self.bot,
                event.message.guild
            )

            print(
                f"Negative vote: message={event.message.id}, "
                f"voter={event.author.id}, "
                f"emote={received_emote}, "
                f"configured_negative={negative_emote}"
            )

        else:
            print(
                f"Ignored reaction: message={event.message.id}, "
                f"voter={event.author.id}, "
                f"emote={received_emote}, "
                f"configured_positive={positive_emote}, "
                f"configured_negative={negative_emote}"
            )


    @interactions.listen(events.MessageReactionRemove)
    async def on_reaction_remove(self, event):
        guild_settings = database.get_server(event.message.guild.id)

        if guild_settings is None:
            return

        received_emote = str(event.emoji)

        if received_emote == guild_settings["vote_positive_emote"]:
            database.remove_vote(
                event.message.id,
                event.author.id,
                1
            )

            print(
                f"Removed positive vote: message={event.message.id}, "
                f"voter={event.author.id}"
            )

        elif received_emote == guild_settings["vote_negative_emote"]:
            database.remove_vote(
                event.message.id,
                event.author.id,
                -1
            )

            print(
                f"Removed negative vote: message={event.message.id}, "
                f"voter={event.author.id}"
            )
        
        await process_any_vote(self.bot, event.message, guild_settings)
