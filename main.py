from aiogram import Router, Dispatcher, Bot
from aiogram.dispatcher import dispatcher
from dotenv import load_dotenv
import asyncio
from os import getenv
import os
from router import router
from filter import callback_router

load_dotenv('token-bot.env')
token = os.getenv("token")

dp = Dispatcher()

dp.include_router(router)
dp.include_router(callback_router)
async def main():
    bot = Bot(token=token)

    print('bot started!')

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

