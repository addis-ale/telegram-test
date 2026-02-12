# Fetching E-commerce Posts from Telegram

## How it works

- **Telegram Bot API** cannot read channel message history. So you **cannot** use a bot to get posts.
- You use the **MTProto API** with a **user account** (your phone number). This is what Telethon does.
- With that, you can read **public channels** (and private ones you’re in).

## 1. Get API credentials

1. Go to **https://my.telegram.org**
2. Log in with your phone number.
3. Open **API development tools**.
4. Click **Create application** and fill in (follow these exactly to avoid errors):
   - **App title** — Letters and numbers only, no spaces/symbols, max 64 characters. Do **not** use the word "telegram". Example: `MyCommerce` or `CommerceAggregator`.
   - **Short name** — **Lowercase letters and numbers only**, 5–32 characters. No underscores, hyphens, or spaces. Example: `mycommerce` or `mycomagg` (if `mycom` gives an error, try a longer or more unique name).
   - **URL** — If the form rejects when empty, use `https://example.com` (you can change it later).
   - **Platform** — You **must** select one; choose **Desktop**.
   - **Description** — Optional.
5. If you still see an error: try in **Incognito/Private** mode, **disable VPN** and **ad blockers**, and use a **more unique short name** (e.g. `mycommerce2025`).
6. After you create it, Telegram **assigns** you:
   - **API ID** — A number (e.g. `12345678`). You **cannot** choose this; copy it.
   - **API Hash** — A long string. You **cannot** choose this; copy it and keep it secret.

## 2. Install and configure

```bash
pip install -r requirements.txt
```

Copy the example config and fill in your values:

```bash
copy config.example.env config.env
```

Edit `config.env`:

- `API_ID` = your API ID
- `API_HASH` = your API hash
- `CHANNEL_USERNAME` = public channel username **without** `@` (e.g. `durov` or your e-commerce channel)

## 3. Run the script

```bash
python fetch_posts.py
```

- **First run:** Telethon will ask for your phone number and the login code Telegram sends you. A session file is saved so you usually don’t need to log in again.
- The script fetches recent messages from the channel and prints them as JSON (text, caption, has_photo, link to post, etc.).

## 4. What you get per post

For each message the script returns things like:

- `id` – message id
- `date` – when it was sent
- `text` / `caption` / `description` – post text (product title, price, description)
- `has_photo` / `has_document` – whether it has image or file
- `url` – link to open the post in Telegram (e.g. `https://t.me/channel_name/123`)

You can then save these to a database and build search on your website.

## Downloading photos (optional)

To actually download the image files from posts, use Telethon’s `download_media()` on each message (see Telethon docs). The script above only checks _whether_ there is a photo; extending it to download and store image URLs or files is the next step for your product catalog.

## Important notes

- Only **public** channels can be read by username. For private channels you must be a member with the same account that runs the script.
- Respect Telegram’s terms and rate limits; avoid very aggressive polling.
- E-commerce content (text, images) may be subject to copyright; linking to the original post is safer than republishing full content.
