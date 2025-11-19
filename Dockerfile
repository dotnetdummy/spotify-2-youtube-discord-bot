FROM python:3.11-slim AS base

# Set working directory
WORKDIR /app

# Install system dependencies (build tools removed after use)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN useradd -m botuser
USER botuser

# Copy bot code
COPY . .

# Environment variable for token
ENV DISCORD_TOKEN=""

# Optional: simple healthcheck (process is running)
HEALTHCHECK CMD pgrep -f "spotify_youtube_bot.py" || exit 1

# Run the bot
CMD ["python", "spotify_youtube_bot.py"]
