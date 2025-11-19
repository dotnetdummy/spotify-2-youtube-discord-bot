import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
from bs4 import BeautifulSoup
import urllib.parse
import os
import re

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------------------------------------------------
# Helper: Fetch HTML
# ---------------------------------------------------------
async def fetch_html(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
            return await resp.text()

# ---------------------------------------------------------
# Track metadata
# ---------------------------------------------------------
async def get_track_metadata(url: str):
    html = await fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")
    og_title = soup.find("meta", property="og:title")
    og_desc = soup.find("meta", property="og:description")
    if not og_title or not og_desc:
        return None
    track = og_title["content"].strip()
    artist = og_desc["content"].replace("Song •", "").strip()
    full_title = f"{track} - {artist}"
    return full_title, track, artist

# ---------------------------------------------------------
# Album metadata
# ---------------------------------------------------------
async def get_album_metadata(url: str):
    html = await fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")
    og_title = soup.find("meta", property="og:title")
    og_desc = soup.find("meta", property="og:description")  # Album • Artist
    if not og_title or not og_desc:
        return None
    album = og_title["content"].strip()
    artist = og_desc["content"].replace("Album •", "").strip()
    full_title = f"{album} - {artist}"
    return full_title, album, artist

# ---------------------------------------------------------
# Playlist metadata
# ---------------------------------------------------------
async def get_playlist_metadata(url: str):
    html = await fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")
    og_title = soup.find("meta", property="og:title")
    if og_title:
        title = og_title["content"].strip()
    else:
        title = "Spotify Playlist"
    return title

# ---------------------------------------------------------
# Build YouTube Music Search URL
# ---------------------------------------------------------
async def yt_music_query(q: str):
    encoded = urllib.parse.quote_plus(q)
    return f"https://music.youtube.com/search?q={encoded}"

# ---------------------------------------------------------
# Detect link type
# ---------------------------------------------------------
def detect_spotify_type(url):
    if "/track/" in url:
        return "track"
    if "/album/" in url:
        return "album"
    if "/playlist/" in url:
        return "playlist"
    return None

# ---------------------------------------------------------
# Process Spotify URL
# ---------------------------------------------------------
async def process_spotify(url: str):
    stype = detect_spotify_type(url)

    if stype == "track":
        meta = await get_track_metadata(url)
        if not meta:
            return None, None
        full_title, track, artist = meta
        yt = await yt_music_query(full_title)
        return f"🎶 Track: **{full_title}**", yt

    if stype == "album":
        meta = await get_album_metadata(url)
        if not meta:
            return None, None
        full_title, album, artist = meta
        yt = await yt_music_query(full_title)
        return f"📀 Album: **{full_title}**", yt

    if stype == "playlist":
        title = await get_playlist_metadata(url)
        yt = await yt_music_query(title)
        return f"🎵 Playlist: **{title}**", yt

    return None, None

# ---------------------------------------------------------
# Auto-detect Spotify links
# ---------------------------------------------------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    match = re.search(r"(https?://open\.spotify\.com/(track|album|playlist)/[^\s]+)", message.content)
    if not match:
        return

    url = match.group(1)
    await message.channel.send("🔎 Processing Spotify link…")

    label, yt = await process_spotify(url)
    if not label:
        return await message.channel.send("❌ Could not process Spotify link.")

    await message.channel.send(f"{label}\n👉 **YouTube Music link:**\n{yt}")

# ---------------------------------------------------------
# Slash command /convert
# ---------------------------------------------------------
@bot.tree.command(name="convert", description="Convert latest Spotify link to YouTube Music")
async def convert_slash(interaction: discord.Interaction):
    msgs = [m async for m in interaction.channel.history(limit=50)]
    url = None
    for m in msgs:
        match = re.search(r"(https?://open\.spotify\.com/(track|album|playlist)/[^\s]+)", m.content)
        if match:
            url = match.group(1)
            break

    if not url:
        return await interaction.response.send_message("No Spotify link found.")

    await interaction.response.send_message("🔎 Processing…")
    label, yt = await process_spotify(url)
    if not label:
        return await interaction.followup.send("❌ Could not extract metadata.")

    await interaction.followup.send(f"{label}\n👉 **YouTube Music link:**\n{yt}")


@bot.event
def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        bot.tree.sync()
    except:
        pass


if TOKEN:
    bot.run(TOKEN)
else:
    print("ERROR: DISCORD_TOKEN environment variable not set.")
