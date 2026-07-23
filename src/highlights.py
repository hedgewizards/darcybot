from src import database
from src.webhookmessages import send_webhook_message


async def process_positive_vote(bot, message, guild_settings):
    score = get_message_score(message.id)

    if score < guild_settings["highlights_threshold"]:
        return

    if database.is_message_highlighted(message.id):
        return

    highlights_channel_id = guild_settings["highlights_channel_id"]

    if highlights_channel_id is None:
        return

    highlights_channel = await message.guild.fetch_channel(
        highlights_channel_id
    )

    await send_webhook_message(
        bot,
        highlights_channel,
        message,
        guild_settings
    )

    database.add_highlighted_message(message.id)


def get_message_score(message_id):
    votes = database.get_votes_for_message(message_id)

    return sum(
        vote[0]
        for vote in votes
    )