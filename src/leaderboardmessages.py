from src import database


async def fix_leaderboard(
    guild,
    guild_settings
):
    leaderboard_channel_id = guild_settings["leaderboard_channel_id"]

    if leaderboard_channel_id is None:
        return

    leaderboard_channel = await guild.fetch_channel(
        leaderboard_channel_id
    )

    leaderboard_message_id = guild_settings["leaderboard_message_id"]

    if leaderboard_message_id:
        try:
            leaderboard_message = await leaderboard_channel.fetch_message(
                leaderboard_message_id
            )

            await update_leaderboard_message(
                leaderboard_message,
                guild_settings
            )

            return

        except Exception:
            pass

    await create_leaderboard_message(
        leaderboard_channel,
        guild_settings
    )


def create_leaderboard_content(
    positive_users,
    negative_users,
    guild_settings
):
    positive_emote = guild_settings["vote_positive_emote"]
    negative_emote = guild_settings["vote_negative_emote"]

    content = (
        f"**🏆{positive_emote} HALL OF FAME {positive_emote}🏆**\n"
    )

    if positive_users:
        for index, (user_id, vote_count) in enumerate(
            positive_users,
            start=1
        ):
            content += (
                f"{index}. <@{user_id}> — "
                f"{positive_emote}x{vote_count}\n"
            )
    else:
        content += "No votes yet.\n"

    content += (
        f"\n**💀{negative_emote} HALL OF SHAME {negative_emote}💀**\n"
    )

    if negative_users:
        for index, (user_id, vote_count) in enumerate(
            negative_users,
            start=1
        ):
            content += (
                f"{index}. <@{user_id}> — "
                f"{negative_emote}x{vote_count}\n"
            )
    else:
        content += "No votes yet.\n"

    return content


async def update_leaderboard_message(
    message,
    guild_settings
):
    leaderboard_size = guild_settings["leaderboard_size"]

    positive_users = database.get_top_voted_users(
        message.guild.id,
        1,
        leaderboard_size
    )

    negative_users = database.get_top_voted_users(
        message.guild.id,
        -1,
        leaderboard_size
    )

    content = create_leaderboard_content(
        positive_users,
        negative_users,
        guild_settings,
    )

    await message.edit(
        content=content
    )


async def create_leaderboard_message(
    channel,
    guild_settings
):
    leaderboard_size = guild_settings["leaderboard_size"]

    positive_users = database.get_top_voted_users(
        channel.guild.id,
        1,
        leaderboard_size
    )

    negative_users = database.get_top_voted_users(
        channel.guild.id,
        -1,
        leaderboard_size
    )

    content = create_leaderboard_content(
        positive_users,
        negative_users,
        guild_settings
    )

    message = await channel.send(
        content=content
    )

    database.set_leaderboard_message_id(
        channel.guild.id,
        message.id
    )