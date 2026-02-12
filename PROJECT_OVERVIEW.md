# Telegram Commerce Aggregator — Project Overview

A one-pager you can share to explain the problem, approach, and stack.

---

## The Problem We're Solving

Today, buying from e-commerce on Telegram works like this:

1. User finds the **right channel** (store) on Telegram.
2. User scrolls that channel to find the **right product**.

**Pain:** There’s no way to search for a product **across many channels**. If you don’t know which channel sells what, you’re stuck browsing channel by channel.

**Goal:** A website where users type what they want (e.g. “wireless earbuds” or “sneakers”) and get results from **all** connected Telegram channels in one place, then open the original post on Telegram to buy.

---

## Our Approach

1. **Aggregate** — We fetch posts from selected public Telegram channels (e.g. stores / marketplaces).
2. **Index** — We store and index post content (title, description, price if we parse it, images, link to Telegram).
3. **Search** — Our website lets users search and filter over this index.
4. **Link** — Each result links to the original Telegram post so the user completes the purchase on Telegram.

We act as a **search layer** on top of Telegram channels; we don’t replace Telegram or handle payments.

---

## Why This Is Feasible

- **Public channels** can be read via Telegram’s **MTProto API** (user client), not the Bot API.
- Libraries like **Telethon** (Python) let us connect with a user account and iterate over channel messages.
- We can run this on a schedule (e.g. every hour) to keep our index updated.
- Storing and searching tens or hundreds of thousands of posts is standard (DB + optional search engine).

**Limits to keep in mind:**

- Only **public** channels (or private ones we’re members of).
- We must respect **Telegram ToS** and **rate limits**.
- **Copyright**: we focus on indexing and linking to the original post rather than republishing full content.

---

## Tech Stack (Current & Planned)

| Layer                   | Choice                                      | Role                                                          |
| ----------------------- | ------------------------------------------- | ------------------------------------------------------------- |
| **Telegram access**     | **Telethon** (Python)                       | MTProto client to fetch channel messages with a user account. |
| **Config**              | **python-dotenv**                           | API credentials and channel list (e.g. `config.env`).         |
| **Backend** (planned)   | **Python** (e.g. FastAPI or Django)         | APIs to list/search products, health checks, admin.           |
| **Database** (planned)  | **PostgreSQL** or **SQLite**                | Store channels, posts, normalized product fields.             |
| **Search** (optional)   | **Postgres full-text** or **Elasticsearch** | Better search and filters as data grows.                      |
| **Frontend** (planned)  | **React / Next.js** or simple HTML          | Search UI, filters, “Open in Telegram” links.                 |
| **Scheduler** (planned) | **Cron** or **Celery** / **APScheduler**    | Periodic job to fetch new posts from channels.                |

Right now we have: **Telethon + script** that fetches posts from one channel and outputs JSON. Next steps: DB, backend API, scheduler, then frontend.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Telegram (public channels)                                 │
└───────────────────────────┬───────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  Our backend (Python)                                       │
│  • Telethon: fetch new messages from channel list           │
│  • Parser: extract title, description, price, media          │
│  • Scheduler: run fetch job every N minutes/hours            │
└───────────────────────────┬───────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  Database + search index                                    │
│  • Channels, posts, product-like fields                     │
└───────────────────────────┬───────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  Our website                                                │
│  • Search box, filters, result cards                        │
│  • Each result → "View on Telegram" → t.me/channel/msg_id   │
└─────────────────────────────────────────────────────────────┘
```

---

## What We Have So Far

- **`fetch_posts.py`** — Fetches the last N messages from a single public channel; returns JSON (id, date, text, has_photo, url).
- **`config.example.env`** — Template for `API_ID`, `API_HASH`, `CHANNEL_USERNAME`.
- **`README.md`** — How to get API keys from my.telegram.org, install deps, and run the script.

To run: get API ID/Hash from [my.telegram.org](https://my.telegram.org), set them in `config.env`, then `python fetch_posts.py`. First run logs in with your phone number (session saved for next time).

---

## Next Steps (Roadmap)

1. **Multi-channel** — Config list of channel usernames; loop and fetch from all.
2. **Database** — Store posts (and optional product schema) in PostgreSQL/SQLite.
3. **Parsing** — Optional: extract price, title, category from post text (regex or simple ML).
4. **Backend API** — Endpoints: search, list by channel, filters.
5. **Scheduler** — Cron or in-process scheduler to refresh channel data periodically.
6. **Frontend** — Search page and result list with “Open in Telegram” links.
7. **Legal / ToS** — Double-check Telegram and local laws; keep “link to source” approach.

---

## One-Liner for Your Friend

**“We’re building a website that indexes e-commerce posts from Telegram channels so users can search for products across all of them in one place, then open the result on Telegram to buy.”**

---

_Last updated: Feb 2025_
