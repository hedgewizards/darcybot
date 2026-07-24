import interactions
from src.database import get_votes_for_message


async def get_webhook(bot, channelId):
    webhooks = await bot.http.get_channel_webhooks(
        channelId
    )

    for webhook in webhooks:
        if webhook["name"] == "Darcy":
            return webhook

    return await bot.http.create_webhook(
        channelId,
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
        guild_settings["highlights_channel_id"]
    )

    payload = get_webhook_payload(message, guild_settings)

    webhook_message = await bot.http.execute_webhook(
        webhook["id"],
        webhook["token"],
        payload,
        wait=True
    )

    print(
        f"Sending webhook message: "
        f"original_message={message.id}, " 
        f"new_message={webhook_message['id']}, "
        f"author={message.author.id}, "
        f"webhook_channel={channel.id}"
    )

    return webhook_message

async def update_webhook_message(
    bot,
    message,
    guild_settings,
    webhook_message_id
):
    webhook = await get_webhook(
        bot,
        guild_settings["highlights_channel_id"]
    )

    payload = get_webhook_payload(message, guild_settings)
    await bot.http.edit_webhook_message(
        webhook["id"],
        webhook["token"],
        webhook_message_id,
        payload
    )
    
    print(
        f"Updating webhook message: "
        f"original_message={message.id}, " 
        f"new_message={webhook_message_id}, "
        f"author={message.author.id}, "
        f"webhook_channel={message.channel.id}"
    )

def get_webhook_message_content(message, guild_settings):
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

    return content

def get_webhook_payload(message, guild_settings):
    return {
        "content": get_webhook_message_content(message, guild_settings),
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