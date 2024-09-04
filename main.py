import os
from fastapi import FastAPI, Request
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Update

app = FastAPI()
bot = AsyncTeleBot(os.getenv('BOT_TOKEN'))

@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    await bot.reply_to(message, "歡迎使用這個機器人!")

@bot.message_handler(func=lambda message: message.text.lower() == '安安')
async def handle_hello(message):
    await bot.reply_to(message, "安安!")

@bot.message_handler(func=lambda message: True)
async def echo_all(message):
    await bot.reply_to(message, message.text)

@app.post("/webhook")
async def webhook(request: Request):
    update = Update.de_json(await request.json())
    await bot.process_new_updates([update])
    return ""

@app.get("/")
async def root():
    return {"message": "Bot is running"}