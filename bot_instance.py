import os
import telebot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("Necesitas configurar TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML", threaded=False)
