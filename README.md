# Spotify to YouTube Music Converter Bot

A Discord bot that automatically converts Spotify links (tracks, albums, playlists) into equivalent YouTube Music search links. The bot monitors messages, extracts metadata from Spotify pages, and provides the closest YouTube Music match.

This project supports:

* 🎵 Spotify **tracks** → YouTube Music
* 📀 Spotify **albums** → YouTube Music
* 🎶 Spotify **playlists** → YouTube Music
* 🤖 Automatic link detection in chat
* 💬 Slash command: `/convert`
* 🐳 Docker support
* 🔒 Environment variable token loading

---

## 🚀 Features

* Converts **tracks**, **albums**, and **playlists**
* Automatically listens for Spotify URLs in any channel
* Uses Open Graph metadata for reliable track/artist extraction
* No external APIs required
* Supports Docker for easy deployment
* Private usage with manual invite URL

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourname/spotify-youtube-discord-bot.git
cd spotify-youtube-discord-bot
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your Discord bot token

The bot uses an environment variable named `DISCORD_TOKEN`.

#### Linux/macOS

```bash
export DISCORD_TOKEN="your_token_here"
```

#### Windows PowerShell

```powershell
setx DISCORD_TOKEN "your_token_here"
```

---

## 🐳 Running with Docker

### Build the image

```bash
docker build -t spotify-youtube-bot .
```

### Run the container

```bash
docker run -e DISCORD_TOKEN="your_token_here" spotify-youtube-bot
```

The optimized Dockerfile includes:

* Non-root user
* Slim Python base image
* Healthcheck
* Automated dependency install

---

## 🐳 Docker Hub Image

A ready‑to‑run Docker image is available on Docker Hub:

**Image:** `dotnetdummy/spotify-2-youtube-discord-bot`

**Link:** [https://hub.docker.com/repository/docker/dotnetdummy/spotify-2-youtube-discord-bot/general](https://hub.docker.com/repository/docker/dotnetdummy/spotify-2-youtube-discord-bot/general)

### 📝 Description

This Docker image contains the fully packaged Spotify → YouTube Music Discord bot with:

* Python 3.11 slim base image
* Non‑root execution
* Healthcheck
* All dependencies pre‑installed

### 🚀 Run it directly

```bash
docker run -e DISCORD_TOKEN="your_token_here" dotnetdummy/spotify-2-youtube-discord-bot:latest
```

---

## 🎮 Usage

### Automatic Conversion

Whenever someone posts a Spotify link (track, album, or playlist), the bot automatically replies with a YouTube Music search link.

### Slash Command

```
/convert
```

Converts the **most recent** Spotify link in the channel history.

---

## 🔧 Configuration

### Required Privileged Intents

Your bot requires:

* **MESSAGE CONTENT INTENT**

Enable it in:

> Developer Portal → Bot → Privileged Gateway Intents

### Add Bot to Your Server

Private bots cannot use Discord's automatic invite generator.
Use this manual invite URL:

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot%20applications.commands&permissions=274878013440
```

Replace `YOUR_CLIENT_ID` with your App ID.

---

## 🛠 Tech Stack

* **Python 3.11**
* **discord.py**
* **aiohttp**
* **BeautifulSoup 4**
* **Docker**

---

## 📜 License

MIT License. Do whatever you like.
