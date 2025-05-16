from aiogram import Bot, Dispatcher
import logging
import asyncio
from aiogram.methods import DeleteWebhook
from app.main import rt
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN=os.getenv("BOT_TOKEN")

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    await bot(DeleteWebhook(drop_pending_updates=True))
    dp.include_router(rt)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())