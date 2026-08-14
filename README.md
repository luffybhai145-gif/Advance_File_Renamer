# Advanced File Renamer

An original Telegram File Renamer and FFmpeg Stream Processing Bot.

## Features

- Rename files
- Remove audio streams
- Remove subtitle streams
- Remove video streams
- Select specific streams
- FFprobe stream detection
- FFmpeg stream copying
- Docker support
- Railway deployment
- Admin-only processing
- Temporary file cleanup

## Commands

/start
/rename

## Environment Variables

API_ID
API_HASH
BOT_TOKEN
ADMIN_IDS
MAX_CONCURRENT_FFMPEG
TEMP_DIR

## Install

pip install -r requirements.txt

## Run

python bot.py

## Docker

docker build -t advanced-file-renamer .

docker run --env-file .env advanced-file-renamer

## Railway

Deploy the repository using Docker.

Railway will detect:

Dockerfile

The Dockerfile installs FFmpeg automatically.

Start command:

python bot.py
