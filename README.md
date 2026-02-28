# Telegram File Rename Bot

A Telegram bot that renames files while preserving their extensions.

## Features
- 📁 Rename any file
- 🔒 Channel join verification
- 🎯 Preserves original extension
- 📊 File info display
- 🚀 Fast processing

## Deploy on Render

1. Fork this repository
2. Create a new Web Service on Render
3. Connect your repository
4. Add environment variable `BOT_TOKEN`
5. Deploy!

## Environment Variables
- `BOT_TOKEN`: Your Telegram bot token

## Commands
- `/start` - Welcome message
- `/cancel` - Cancel current operation
- `/status` - Check bot status

## Requirements
- Python 3.8+
- pyTelegramBotAPI
- python-dotenv

## Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your bot token
echo "BOT_TOKEN=your_token_here" > .env

# Run bot
python bot.py
