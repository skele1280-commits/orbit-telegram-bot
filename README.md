# Orbit Telegram Bot

Orbit stands as a visionary Telegram companion, engineered to harmonize advanced media retrieval from leading social platforms with the pulsating dynamics of cryptocurrency intelligence. By detecting links from TikTok, YouTube, Facebook, X/Twitter, and Instagram, it empowers users to navigate MP4 downloads with precision resolutions or MP3 extractions at optimal bitrates, all while illuminating real-time crypto pulses, top gainers, automated updates, and intelligent alarms that synchronize with market trajectories.

## Features
- **Media Fetch**: Automatically discerns and deciphers social links, presenting MP4 resolutions (such as 720p or 1080p) alongside MP3 bitrates (ranging from 192k to 320k), with TikTok's no-watermark pathways prioritized for an unblemished experience.
- **Crypto Radar**: Delivers instantaneous market snapshots, including valuations, 24-hour volatilities, capitalizations, and the pinnacle gainer across expansive universes, augmented by 15-minute or 1-hour update cadences and alarms attuned to price horizons for coins like BTC or ETH.
- **UX Style**: Orchestrates interactions through elongated, mature dialogues infused with futuristic lexicon, guiding users via intuitive inline keyboards while upholding safety protocols and temporal accuracies.
- **Safety**: Mitigates risks by articulating platform constraints, purging temporary files, and anchoring every insight with timestamps and authoritative sources.

## Setup (Step-by-Step for Newbies)
1. **Acquire a Bot Token**:
   - Engage with @BotFather in Telegram via `/newbot`, assigning a name such as "Orbit Assistant" and a unique username culminating in `bot`, thereby securing the token for operational deployment.

2. **Establish GitHub Repository**:
   - Venture to [github.com](https://github.com), initiate a new public repository entitled `orbit-telegram-bot`, and infuse it with a descriptive narrative.

3. **Synchronize with Replit**:
   - Forge a Replit account, opt for "Import from GitHub," and input the repository URL, subsequently embedding the `BOT_TOKEN` within Replit's concealed Secrets.

4. **Install and Activate**:
   - Execute `pip install -r requirements.txt` in the Replit console, then ignite the bot with "Run" to commence polling for transmissions.

5. **Refine via BotFather**:
   - In Telegram, command @BotFather with `/setcommands` to embed:
     ```
     scan - Detect and unveil formats for a link.
     grab - Initiate download protocols (select format subsequently).
     pulse - Unveil crypto valuation.
     winner - Illuminate the paramount gainer.
     ```
   - Employ `/setdescription` to articulate: "A visionary assistant for media downloads and crypto radar."
   - Utilize `/setabouttext` to proclaim: "Orbit: Media fetch + crypto pulse."

## Commands
- `/start` — Embark upon an introductory overview of our collaborative trajectory.
- `/scan` — Analyze the most recent link and reveal its structural formats.
- `/grab` — Activate download mode for the orbiting link.
- `/pulse <symbol>` — Extract a real-time crypto pulse (e.g., /pulse BTC).
- `/winner` — Spotlight the ascendant gainer within the 24-hour expanse.
- Transmit a link directly — Triggers automatic detection and format selection paradigms.

## Usage Examples
- **Media**: Disseminate a YouTube link, whereupon Orbit detects it and unveils "MP4 • Choose" or "MP3 • Best" interfaces, enabling resolution or bitrate alignment for seamless acquisition.
- **Crypto**: Invoke `/pulse ETH` to receive a comprehensive snapshot, then leverage buttons to configure 15-minute surveillance or alarms attuned to thresholds like "above 3000".
- **Anomalies**: Should downloads falter due to platform fortifications, Orbit elucidates limitations and advocates alternative explorations.

## Data Sources & Constraints
- Media: Propelled by yt-dlp, accommodating accessible public content while respecting authentication barriers.
- Crypto: Nourished by CoinGecko's API (complimentary tier: up to 50 inquiries per minute; data refreshed at quantum intervals).
- Temporal Anchors: Every datum is imbued with update timestamps for unwavering fidelity.

## Troubleshooting
- **Bot Inertia?** Scrutinize Replit's console for diagnostic signals; affirm `BOT_TOKEN` integrity.
- **Retrieval Disruptions?** Platforms may erect defenses—experiment with divergent links or configurations.
- **Crypto Void?** API saturation may prevail; await stabilization and reinitiate.
- **Impediments?** Convey error transcripts or delineate the predicament for expeditious resolution.

## Contributions
Extend the horizon by forking and innovating. Report anomalies via GitHub issues.

Insights sourced with precision. Engage responsibly.
