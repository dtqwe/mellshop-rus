import asyncio
from aiogram import Bot, Dispatcher, F
from app.handlers import router
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

admin_id = int(os.getenv('ADMIN_ID'))
TOKEN = os.getenv('TOKEN')

async def main():
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Выход")