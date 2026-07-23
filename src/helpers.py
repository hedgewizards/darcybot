def format_channel(channel_id):
    if channel_id is None:
        return "None"

    return f"<#{channel_id}>"