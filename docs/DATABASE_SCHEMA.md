# What to Store in the Database

A simple schema for the Telegram commerce aggregator: what to store and why.

---

## 1. Table: `channels`

Stores the list of Telegram channels you aggregate from.

| Column            | Type                | Why                                                       |
| ----------------- | ------------------- | --------------------------------------------------------- |
| `id`              | PK (int/uuid)       | Internal ID.                                              |
| `username`        | string, unique      | Telegram channel username (no `@`), e.g. `dagilaptop`.    |
| `title`           | string, optional    | Channel display name (from Telegram).                     |
| `last_fetched_at` | timestamp, optional | When we last synced this channel (for incremental fetch). |
| `created_at`      | timestamp           | When we added the channel.                                |

---

## 2. Table: `posts`

Stores each post you fetch. One row per Telegram message.

| Column                | Type          | Why                                                                            |
| --------------------- | ------------- | ------------------------------------------------------------------------------ |
| `id`                  | PK (int/uuid) | Internal ID.                                                                   |
| `channel_id`          | FK → channels | Which channel this post is from.                                               |
| `telegram_message_id` | int           | Message ID on Telegram (unique per channel).                                   |
| `text`                | text          | **Full message/caption text** — this is what you **search** on.                |
| `posted_at`           | timestamp     | When the post was published on Telegram.                                       |
| `url`                 | string        | `https://t.me/{username}/{telegram_message_id}` — link for "View on Telegram". |
| `has_photo`           | boolean       | Whether the post has a photo (for showing thumbnail placeholder).              |
| `has_document`        | boolean       | Whether it has a file attachment.                                              |
| `views`               | int, optional | View count from Telegram, if you want to sort by popularity.                   |
| `created_at`          | timestamp     | When we inserted the row.                                                      |

**Unique constraint:** `(channel_id, telegram_message_id)` so you don’t insert the same post twice.

---

## 3. Optional columns (for better search/filters)

If you want to filter by price or show a “title” in results, parse the post `text` and store:

| Column  | Type              | Why                                                                  |
| ------- | ----------------- | -------------------------------------------------------------------- |
| `price` | decimal, nullable | Parsed from text (e.g. "₹5000" / "$50"). Enables price-range filter. |
| `title` | string, nullable  | First line or first N chars of `text` — nicer result titles.         |

You can add these later; search still works with `text` only.

---

## 4. What you don’t need to store

- **Images** — Don’t store image bytes. Use “View on Telegram” or Telegram’s embed; optionally store a thumbnail URL later if Telegram exposes one.
- **Full HTML** — Plain `text` is enough for search and display.
- **User data** — You’re not logging in users (unless you add accounts later).

---

## 5. Summary

| Table        | What it’s for                                                                                            |
| ------------ | -------------------------------------------------------------------------------------------------------- |
| **channels** | List of channels you track; link posts to a channel.                                                     |
| **posts**    | Every post: **text** (for search), **url** (for link), **posted_at**, channel, and optional price/title. |

Search = full-text search on `posts.text` (and optional filter by `channel_id`, `price`, `posted_at`). That’s what you need to store.
