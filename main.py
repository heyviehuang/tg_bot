import os
import logging
from fastapi import FastAPI, Request
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Update

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    try:
        update = Update.de_json(await request.json())
        await bot.process_new_updates([update])
    except Exception as e:
        logger.error(f"Error processing update: {e}")
        return {"error": str(e)}
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Bot is running"}

# 添加一个错误处理器
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return {"error": "An unexpected error occurred"}

# 添加一个健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "healthy"}