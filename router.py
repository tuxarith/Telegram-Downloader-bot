from aiogram import Router, Dispatcher, Bot
import asyncio
from aiogram.filters import Command
from aiogram.types import message, Message, FSInputFile
from buttons import url_github

router = Router()

@router.message(Command('start'))
async def start(message: Message):
    await message.answer("Привет! Это бот для скачивания видео по сыллкам Tiktok и Youtube. Используй команды get <СЫЛЛКА> чтобы заполучить видео")


@router.message(Command('github'))
async def github(message: Message):
    photo = FSInputFile('photo/photo_2026-09-06_19-01-08.jpg')
    await message.answer_photo(photo=photo, reply_markup=url_github())






