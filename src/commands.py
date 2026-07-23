import discord
from discord import app_commands

from src import database


def setup_commands(bot):

    @bot.tree.command(name="set-leaderboard")
    @app_commands.describe(
        channel="The channel where the leaderboard will be displayed"
    )
    async def set_leaderboard(
        interaction: discord.Interaction,
        channel: discord.TextChannel
    ):
        database.set_leaderboard_channel(
            interaction.guild_id,
            channel.id
        )

        await interaction.response.send_message(
            f"Leaderboard channel set to {channel.mention}."
        )


    @bot.tree.command(name="set-highlights")
    @app_commands.describe(
        channel="The channel where highlights will be posted"
    )
    async def set_highlights(
        interaction: discord.Interaction,
        channel: discord.TextChannel
    ):
        database.set_highlights_channel(
            interaction.guild_id,
            channel.id
        )

        await interaction.response.send_message(
            f"Highlights channel set to {channel.mention}."
        )


    @bot.tree.command(name="set-vote-emotes")
    @app_commands.describe(
        positive="The positive vote emoji",
        negative="The negative vote emoji"
    )
    async def set_emotes(
        interaction: discord.Interaction,
        positive: str,
        negative: str
    ):
        database.set_vote_emotes(
            interaction.guild_id,
            positive,
            negative
        )

        await interaction.response.send_message(
            f"Vote emotes set to {positive} and {negative}."
        )


    @bot.tree.command(name="set-highlights-threshold")
    @app_commands.describe(
        threshold="The minimum score required for a highlight"
    )
    async def set_threshold(
        interaction: discord.Interaction,
        threshold: int
    ):
        database.set_highlights_threshold(
            interaction.guild_id,
            threshold
        )

        await interaction.response.send_message(
            f"Highlights threshold set to {threshold}."
        )
    
    @bot.tree.command(name="clear-leaderboard")
    async def clear_leaderboard(
        interaction: discord.Interaction
    ):
        database.set_leaderboard_channel(
            interaction.guild_id,
            None
        )

        await interaction.response.send_message(
            "Leaderboard channel cleared."
        )


    @bot.tree.command(name="clear-highlights")
    async def clear_highlights(
        interaction: discord.Interaction
    ):
        database.set_highlights_channel(
            interaction.guild_id,
            None
        )

        await interaction.response.send_message(
            "Highlights channel cleared."
        )