import os
import re
import uuid
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import yt_dlp

# Constants
TOKEN = os.environ.get("BOT_TOKEN")
COINGECKO_BASE = "https://api.coingecko.com/api/v3"

# Global: Store last link per user for quick commands
last_links = {}

# Helper: Detect platform from URL
def detect_platform(url):
    if any(domain in url for domain in ["tiktok.com", "vm.tiktok.com", "vt.tiktok.com"]):
        return "TikTok"
    elif any(domain in url for domain in ["youtube.com", "youtu.be"]):
        return "YouTube"
    elif any(domain in url for domain in ["facebook.com", "fb.watch"]):
        return "Facebook"
    elif any(domain in url for domain in ["x.com", "twitter.com"]):
        return "X/Twitter"
    elif any(domain in url for domain in ["instagram.com"]):
        return "Instagram"
    return None

# Helper: Scan message for URLs
def scan_urls(text):
    return re.findall(r'https?://[^\s]+', text)

# Helper: Probe media (simulate tool)
def media_probe(url):
    platform = detect_platform(url)
    if not platform:
        return None
    # Basic probe (in real tool, use yt_dlp to get formats)
    ydl_opts = {"quiet": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])
            mp4_resolutions = sorted(set(f.get("height") for f in formats if f.get("vcodec") != "none" and f.get("height")), reverse=True)
            mp3_bitrates = sorted(set(f.get("abr") for f in formats if f.get("acodec") != "none" and f.get("abr")), reverse=True)
            return {
                "platform": platform,
                "type": "video" if mp4_resolutions else "audio",
                "mp4_resolutions": [f"{r}p" for r in mp4_resolutions[:5]],  # Limit to top 5
                "mp3_bitrates": [f"{b}k" for b in mp3_bitrates[:3]] if mp3_bitrates else ["Best"]
            }
    except:
        return None

# Helper: Fetch media (simulate tool)
def media_fetch(url, format_type, resolution=None, bitrate=None, watermark="no_watermark"):
    file_id = uuid.uuid4().hex
    outtmpl = f"media_{file_id}.%(ext)s"
    ydl_opts = {
        "format": "best" if format_type == "mp4" else "bestaudio/best",
        "outtmpl": outtmpl,
        "noplaylist": True,
        "quiet": True,
    }
    if resolution and format_type == "mp4":
        ydl_opts["format"] = f"best[height<={resolution[:-1]}]"
    if bitrate and format_type == "mp3":
        ydl_opts["format"] = f"bestaudio[abr<={bitrate[:-1]}]"
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            path = ydl.prepare_filename(info)
            return path
    except:
        return None

# Helper: Crypto quote (simulate tool)
def crypto_quote(symbol):
    try:
        response = requests.get(f"{COINGECKO_BASE}/simple/price", params={
            "ids": symbol.lower(),
            "vs_currencies": "usd",
            "include_24hr_change": True,
            "include_24hr_high": True,
            "include_24hr_low": True,
            "include_market_cap": True
        }, timeout=10)
        data = response.json().get(symbol.lower(), {})
        return {
            "price": data.get("usd"),
            "low_24h": data.get("usd_24h_low"),
            "high_24h": data.get("usd_24h_high"),
            "mcap": data.get("usd_market_cap"),
            "change_24h": data.get("usd_24h_change"),
            "source": "CoinGecko"
        }
    except:
        return None

# Helper: Top gainer (simulate tool)
def crypto_top_gainer(universe="top_100"):
    try:
        response = requests.get(f"{COINGECKO_BASE}/coins/markets", params={
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 100,
            "price_change_percentage": "24h"
        }, timeout=10)
        coins = response.json()
        top = max(coins, key=lambda x: x.get("price_change_percentage_24h", 0))
        return {
            "symbol": top["symbol"].upper(),
            "name": top["name"],
            "change_pct": top["price_change_percentage_24h"]
        }
    except:
        return None

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Orbit online. Send a social link or use /pulse for crypto. Let's navigate the web."
    )

# Command: /scan
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in last_links or not last_links[user_id]:
        await update.message.reply_text("No link to scan. Send one first.")
        return
    url = last_links[user_id]
    probe = media_probe(url)
    if not probe:
        await update.message.reply_text("Couldn't scan this link. Platform not supported.")
        return
    msg = f"Scanned: {probe['platform']} • {probe['type']}\n\nChoose output:"
    keyboard = [
        [InlineKeyboardButton("MP4 • Choose", callback_data=f"mp4_choose_{url}")],
        [InlineKeyboardButton("MP3 • Best", callback_data=f"mp3_fetch_{url}_best")]
    ]
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))

# Command: /grab
async def grab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in last_links:
        await update.message.reply_text("No link detected. Send one.")
        return
    url = last_links[user_id]
    probe = media_probe(url)
    if not probe:
        await update.message.reply_text("Link not supported.")
        return
    keyboard = [
        [InlineKeyboardButton("MP4 • Choose", callback_data=f"mp4_choose_{url}")],
        [InlineKeyboardButton("MP3 • Best", callback_data=f"mp3_fetch_{url}_best")]
    ]
    await update.message.reply_text("Grab mode. Pick format:", reply_markup=InlineKeyboardMarkup(keyboard))

# Command: /pulse
async def pulse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Send a symbol like: /pulse BTC")
        return
    symbol = context.args[0].upper()
    quote = crypto_quote(symbol)
    if not quote:
        await update.message.reply_text("Couldn't fetch data. Check symbol.")
        return
    msg = f"{symbol} • Live snapshot\n\nPrice: ${quote['price']:,.2f}\n24h Low/High: ${quote['low_24h']:,.2f} / ${quote['high_24h']:,.2f}\nMarket Cap: ${quote['mcap']:,.0f}\n24h Change: {quote['change_24h']:.2f}%\n\nSource: {quote['source']}"
    keyboard = [
        [InlineKeyboardButton("Track • 15m", callback_data=f"track_15m_{symbol}")],
        [InlineKeyboardButton("Track • 1h", callback_data=f"track_1h_{symbol}")],
        [InlineKeyboardButton("Set Alarm", callback_data=f"alarm_{symbol}")]
    ]
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))

# Command: /winner
async def winner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gainer = crypto_top_gainer()
    if not gainer:
        await update.message.reply_text("No data available.")
        return
    await update.message.reply_text(f"Top gainer: {gainer['name']} ({gainer['symbol']}) • +{gainer['change_pct']:.2f}%")

# Handle messages (auto-detect links)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    urls = scan_urls(text)
    if urls:
        url = urls[0]  # Handle first link
        platform = detect_platform(url)
        if platform:
            user_id = update.effective_user.id
            last_links[user_id] = url
            probe = media_probe(url)
            if probe:
                msg = f"Link detected: {platform} • {probe['type']}\n\nChoose output:"
                keyboard = [
                    [InlineKeyboardButton("MP4 • Choose", callback_data=f"mp4_choose_{url}")],
                    [InlineKeyboardButton("MP3 • Best", callback_data=f"mp3_fetch_{url}_best")]
                ]
                await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                await update.message.reply_text("Link scanned, but couldn't probe formats.")
        else:
            await update.message.reply_text("Platform not supported.")
    else:
        await update.message.reply_text("No link found. Try /scan or send a URL.")

# Handle inline button callbacks
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("mp4_choose_"):
        url = data.split("_", 2)[2]
        probe = media_probe(url)
        if probe and probe["mp4_resolutions"]:
            keyboard = [[InlineKeyboardButton(f"MP4 • {res}", callback_data=f"mp4_fetch_{url}_{res}")] for res in probe["mp4_resolutions"]]
            keyboard.append([InlineKeyboardButton("Back", callback_data=f"back_to_choose_{url}")])
            await query.edit_message_text("Pick resolution:", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.edit_message_text("No MP4 options available.")
    elif data.startswith("mp4_fetch_"):
        parts = data.split("_", 3)
        url, res = parts[2], parts[3]
        await query.edit_message_text("Fetching MP4...")
        path = media_fetch(url, "mp4", resolution=res)
        if path:
            with open(path, "rb") as f:
                await query.message.reply_video(video=f)
            os.remove(path)
        else:
            await query.edit_message_text("Download failed. Try another resolution.")
    elif data.startswith("mp3_fetch_"):
        url = data.split("_", 2)[2]
        await query.edit_message_text("Fetching MP3...")
        path = media_fetch(url, "mp3")
        if path:
            with open(path, "rb") as f:
                await query.message.reply_audio(audio=f)
            os.remove(path)
        else:
            await query.edit_message_text("Download failed.")
    elif data.startswith("track_"):
        parts = data.split("_", 2)
        cadence, symbol = parts[1], parts[2]
        # Simulate subscription (in real bot, store per user)
        await query.edit_message_text(f"Tracking {symbol} every {cadence}. Updates will come.")
    elif data.startswith("alarm_"):
        symbol = data.split("_", 1)[1]
        await query.edit_message_text(f"Alarm for {symbol}: Reply with 'above 50000' or 'below 40000'.")

# Main
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("scan", scan))
    application.add_handler(CommandHandler("grab", grab))
    application.add_handler(CommandHandler("pulse", pulse))
    application.add_handler(CommandHandler("winner", winner))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.run_polling()
