import interactions
from src.database import get_votes_for_message


async def get_webhook(bot, channel):
    webhooks = await bot.http.get_channel_webhooks(
        channel.id
    )

    for webhook in webhooks:
        if webhook["name"] == "Darcy":
            return webhook

    return await bot.http.create_webhook(
        channel.id,
        name="Darcy"
    )

async def send_webhook_message(
    bot,
    channel,
    message,
    guild_settings
):
    webhook = await get_webhook(
        bot,
        channel
    )

    content = message.content or ""

    if message.attachments:
        attachment_links = "\n".join(
            attachment.url
            for attachment in message.attachments
        )

        if content:
            content += "\n" + attachment_links
        else:
            content = attachment_links
    
    if content == "":
        content = "<no content>"

    votes = get_votes_for_message(message.id)

    positive_votes = sum(
        1 for vote in votes
        if vote[0] == 1
    )

    negative_votes = sum(
        1 for vote in votes
        if vote[0] == -1
    )

    content += (
        f"\n\n{guild_settings['vote_positive_emote']} x{positive_votes}"
        f"\n{guild_settings['vote_negative_emote']} x{negative_votes}"
    )

    payload = {
        "content": content,
        "username": message.author.display_name,
        "avatar_url": message.author.avatar.url,
        "allowed_mentions": {
            "parse": [],
            "replied_user": "false"
        },
        "components": [
            {
                "type": 1,
                "components": [
                    {
                        "type": 2,
                        "style": 5,
                        "label": "View Original",
                        "url": message.jump_url
                    }
                ]
            }
        ]
    }

    await bot.http.execute_webhook(
        webhook["id"],
        webhook["token"],
        payload
    )