import interactions


async def get_webhook(channel):
    webhooks = await channel.webhooks()

    for webhook in webhooks:
        if webhook.name == "Darcy":
            return webhook

    return await channel.create_webhook(
        name="Darcy"
    )


async def send_webhook_message(
    channel,
    message,
):
    webhook = await get_webhook(channel)

    await webhook.send(
        content=message.content,
        username=message.author.display_name,
        avatar_url=message.author.avatar.url,
    )