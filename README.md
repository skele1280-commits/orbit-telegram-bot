# Orbit Telegram Bot

A sleek, futuristic Telegram assistant designed for seamless media downloads and crypto insights. Orbit detects social links (TikTok, YouTube, Facebook, X/Twitter, Instagram) and guides you through MP4/MP3 downloads with quality choices. It also provides real-time crypto quotes, top gainers, scheduled updates, and price alarms—pulled fresh from reliable sources.

## Features
- **Media Fetch**: Auto-detects links and offers MP4 resolutions (e.g., 720p, 1080p) or MP3 bitrates (e.g., 192k, 320k). Supports TikTok no-watermark options where available.
- **Crypto Radar**: Instant quotes (price, 24h low/high, market cap), top gainer tracking, 15m/1h updates, and customizable alarms for coins like BTC or ETH.
- **UX Style**: Guided flows with inline buttons for quick choices. Short, confident responses with timestamps and sources.
- **Safety**: Handles blocked platforms, cleans up files, and confirms actions to avoid surprises.

## Setup (Step-by-Step for Newbies)
1. **Get a Bot Token**:
   - Open Telegram, search for @BotFather, and type `/newbot`.
   - Follow prompts to name your bot (e.g., "Orbit Assistant") and get the token (save it safely—it's like a password).

2. **Create GitHub Repo**:
   - Go to [github.com](https://github.com), log in, and create a new repository named `orbit-telegram-bot`.
   - Set visibility to Public. Skip README/.gitignore for now.

3. **Sync to Replit**:
   - Go to [replit.com](https://replit.com), create an account, and click "Create" > "Import from GitHub."
   - Paste your repo URL (e.g., `https://github.com/yourusername/orbit-telegram-bot.git`).
   - In Replit's "Secrets" tab, add `BOT_TOKEN` as the key and your token as the value.

4. **Install and Run**:
   - In Replit's shell (bottom panel), run: `pip install -r requirements.txt`
   - Click "Run" to start the bot. It will poll for messages.

5. **Polish with BotFather**:
   - In Telegram, go to @BotFather and run `/setcommands`.
   - Select your bot and paste:
     ```
     scan - Detect and show formats for a link.
     grab - Download media (choose format next).
     pulse - Get crypto quote.
     winner - Show top gainer.
     ```
   - Run `/setdescription` and paste: "A futuristic assistant for media downloads and crypto radar."
   - Run `/setabouttext` and paste: "Orbit: Media fetch + crypto pulse."

## Commands
- `/start` — Welcome and overview.
- `/scan` — Analyze the last link and show formats.
- `/grab` — Start download mode for the last link.
- `/pulse <symbol>` — Real-time crypto quote (e.g., /pulse BTC).
- `/winner` — Top gainer in 24h.
- Send a link directly — Auto-detects and offers options.

## Usage Examples
- **Media**: Paste a YouTube link. Orbit detects it and shows "MP4 • Choose" or "MP3 • Best" buttons. Pick a resolution/bitrate to download.
- **Crypto**: Type `/pulse ETH` for a snapshot. Use buttons to set 15m updates or alarms (e.g., "above 3000").
- **Errors**: If a site blocks downloads, Orbit explains limits and suggests alternatives.

## Data Sources & Limits
- Media: Powered by yt-dlp (supports most public links; no login-required content).
- Crypto: CoinGecko API (free tier: ~50 calls/minute; data updates every few minutes).
- Timestamps: All data includes update times. Alarms/updates are per-user and stored in-memory (resets on restart).

## Troubleshooting
- **Bot not responding?** Check Replit console for errors. Ensure BOT_TOKEN is correct.
- **Download fails?** Platform may block bots—try a different link or resolution.
- **Crypto data missing?** API rate-limit; wait and retry.
- **Stuck?** Paste errors here or describe the issue—I'll help debug.

## Contributing
Feel free to fork and enhance! For issues, open a GitHub issue.

Data sourced responsibly. Use at your own risk.
