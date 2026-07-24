import asyncio

from src import database
from src import leaderboardmessages


_update_tasks = {}


def trigger_update_leaderboard(bot, guild):
    server_id = guild.id

    existing_task = _update_tasks.get(server_id)

    if existing_task is not None:
        existing_task.cancel()

    _update_tasks[server_id] = asyncio.create_task(
        _debounced_update(
            bot,
            guild
        )
    )


async def _debounced_update(bot, guild):
    server_id = guild.id

    try:
        await asyncio.sleep(10)

        settings = database.get_server(server_id)

        if settings is None:
            return

        await leaderboardmessages.fix_leaderboard(
            guild,
            settings
        )

    except asyncio.CancelledError:
        pass

    finally:
        _update_tasks.pop(server_id, None)