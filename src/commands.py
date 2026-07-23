from interactions import (
    Extension,
    slash_command,
    slash_option,
    OptionType,
    Permissions
)
from src.helpers import format_channel

from src import database


class Commands(Extension):

    @slash_command(
        name="display-current-settings",
        description="Display the current server settings",
        default_member_permissions=Permissions.ADMINISTRATOR
    )

    async def display_current_settings(self, ctx):
        settings = database.get_server(ctx.guild_id)

        await ctx.send(
            f"**Current Server Settings**\n"
            f"Leaderboard Channel: {format_channel(settings['leaderboard_channel_id'])}\n"
            f"Highlights Channel: {format_channel(settings['highlights_channel_id'])}\n"
            f"Positive Vote: {settings['vote_positive_emote']}\n"
            f"Negative Vote: {settings['vote_negative_emote']}\n"
            f"Highlights Threshold: {settings['highlights_threshold']}"
        )

    @slash_command(
        name="set-leaderboard",
        description="Set the leaderboard channel",
        default_member_permissions=Permissions.ADMINISTRATOR
    )
    @slash_option(
        name="channel",
        description="The channel where the leaderboard will be displayed",
        opt_type=OptionType.CHANNEL,
        required=True
    )
    async def set_leaderboard(self, ctx, channel):
        database.set_leaderboard_channel(
            ctx.guild_id,
            channel.id
        )

        await ctx.send(
            f"Leaderboard channel set to {channel.mention}."
        )


    @slash_command(
        name="set-highlights",
        description="Set the highlights channel",
        default_member_permissions=Permissions.ADMINISTRATOR
    )
    @slash_option(
        name="channel",
        description="The channel where highlights will be posted",
        opt_type=OptionType.CHANNEL,
        required=True
    )
    async def set_highlights(self, ctx, channel):
        database.set_highlights_channel(
            ctx.guild_id,
            channel.id
        )

        await ctx.send(
            f"Highlights channel set to {channel.mention}."
        )


    @slash_command(
        name="set-vote-emotes",
        description="Set the positive and negative vote emotes",
        default_member_permissions=Permissions.ADMINISTRATOR
    )
    @slash_option(
        name="positive",
        description="The positive vote emoji",
        opt_type=OptionType.STRING,
        required=True
    )
    @slash_option(
        name="negative",
        description="The negative vote emoji",
        opt_type=OptionType.STRING,
        required=True
    )
    async def set_emotes(self, ctx, positive, negative):
        database.set_vote_emotes(
            ctx.guild_id,
            positive,
            negative
        )

        await ctx.send(
            f"Vote emotes set to {positive} and {negative}."
        )


    @slash_command(
        name="set-highlights-threshold",
        description="Set the minimum score required for a highlight",
        default_member_permissions=Permissions.ADMINISTRATOR
    )
    @slash_option(
        name="threshold",
        description="The minimum score required for a highlight",
        opt_type=OptionType.INTEGER,
        required=True
    )
    async def set_threshold(self, ctx, threshold):
        database.set_highlights_threshold(
            ctx.guild_id,
            threshold
        )

        await ctx.send(
            f"Highlights threshold set to {threshold}."
        )


    @slash_command(
        name="clear-leaderboard",
        description="Stop updating the leaderboards channel",
        default_member_permissions=Permissions.ADMINISTRATOR
    )
    async def clear_leaderboard(self, ctx):
        database.set_leaderboard_channel(
            ctx.guild_id,
            None
        )

        await ctx.send(
            "Leaderboard channel cleared."
        )


    @slash_command(
        name="clear-highlights",
        description="Stop displaying highlights",
        default_member_permissions=Permissions.ADMINISTRATOR
    )
    async def clear_highlights(self, ctx):
        database.set_highlights_channel(
            ctx.guild_id,
            None
        )

        await ctx.send(
            "Highlights channel cleared."
        )


def format_channel(channel_id):
    if channel_id is None:
        return "None"

    return f"<#{channel_id}>"