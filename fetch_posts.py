"""
Fetch e-commerce style posts from a Telegram public channel.
Uses Telethon (MTProto) - you must run with a user account (phone login).
Bots cannot read channel message history.
"""

import os
import asyncio
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

# Load from env or config
def get_env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


async def fetch_channel_posts(channel_username: str, limit: int = 50):
    """
    Fetch recent posts from a public channel.
    channel_username: e.g. "durov" or "telegram" (no @)
    """
    api_id = get_env("API_ID")
    api_hash = get_env("API_HASH")
    if not api_id or not api_hash:
        raise ValueError(
            "Set API_ID and API_HASH (from https://my.telegram.org/apps) in config.env or environment"
        )

    # Session file keeps you logged in so you don't re-enter code every time
    client = TelegramClient("session_name", int(api_id), api_hash)
    await client.start()  # Will prompt for phone + code on first run

    posts = []
    async for message in client.iter_messages(channel_username, limit=limit):
        # message.text is the main text; with photos, product text is often in the caption
        text = (message.text or "") or (getattr(message, "message", "") or "")
        if not text.strip() and not message.media:
            continue
        post = {
            "id": message.id,
            "date": message.date.isoformat() if message.date else None,
            "text": text,
            "has_photo": isinstance(message.media, MessageMediaPhoto),
            "has_document": isinstance(message.media, MessageMediaDocument),
            "views": getattr(message, "views", None),
            "url": f"https://t.me/{channel_username}/{message.id}",
        }
        posts.append(post)

    await client.disconnect()
    return posts


async def main():
    import json
    channel = get_env("CHANNEL_USERNAME", "durov")
    limit = int(get_env("LIMIT", "20"))
    print(f"Fetching last {limit} messages from @{channel}...")
    posts = await fetch_channel_posts(channel, limit=limit)
    print(json.dumps(posts, indent=2, ensure_ascii=False))
    print(f"\nTotal: {len(posts)} posts")


if __name__ == "__main__":
    # Load .env if you use python-dotenv
    try:
        from dotenv import load_dotenv
        load_dotenv("config.env")
    except ImportError:
        pass
    asyncio.run(main())
