# Telegram RSS Alert Bot

This bot monitors a specified RSS feed and sends Telegram alerts when keywords are detected in article titles.

## Environment Variables
- `BOT_TOKEN`: Your Telegram Bot token
- `CHAT_ID`: Your Telegram Chat ID
- `RSS_FEED_URL`: The RSS feed URL to monitor
- `KEYWORDS`: Comma-separated list of keywords to filter article titles

## Endpoints
- `/`: Health check
- `/test`: Sends a test message to Telegram

## Deployment
This project is designed to work seamlessly on Railway with proper environment variables set.