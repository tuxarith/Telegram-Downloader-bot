from buttons import main_inline_keyboard, quality_inline_keyboard
from aiogram.types import callback_query, CallbackQuery, message, Message, FSInputFile
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from func import download, download_all
import os
import random
import gallery_dl

callback_router = Router()


@callback_router.callback_query(lambda c: c.data == 'no_volume')
async def no_volume_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    current_status = data.get('no_volume', False)

    new_status = not current_status

    await state.update_data(no_volume=new_status)

    update_keyboard = main_inline_keyboard(no_volume=new_status)

    await callback.message.edit_reply_markup(reply_markup=update_keyboard)
    await callback.answer()


@callback_router.callback_query(lambda c: c.data == 'image')
async def image_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    current_status = data.get('image', False)

    new_status = not current_status

    await state.update_data(image=new_status)

    update_keyboard = main_inline_keyboard(image=new_status)

    await callback.message.edit_reply_markup(reply_markup=update_keyboard)

    await callback.answer()


@callback_router.callback_query(lambda c: c.data == 'mp3')
async def mp3_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    current_status = data.get('mp3', False)

    new_status = not current_status

    update_keyboard = main_inline_keyboard(mp3=new_status)

    await state.update_data(mp3=new_status)

    await callback.message.edit_reply_markup(reply_markup=update_keyboard)
    await callback.answer()


@callback_router.callback_query(lambda c: c.data == 'get')
async def get(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    url = data.get('video_url')
    no_volume = data.get('no_volume', False)
    mp3 = data.get('mp3', False)
    image = data.get('image', False)
    quality = data.get('quality', 360)
    await state.update_data(url=url, no_volume=False, mp3=False, image=False)

    if not url:
        await callback.message.answer("Not a url. Please send the url ")
        await callback.answer()
        return

    await callback.answer("Сборка файла Запущена... ")

    if isinstance(url, str):
        url = url.strip("[]'\" ")
    elif isinstance(url, list) and len(url) > 0:
        url = str(url[0]).strip("[]'\" ")

    await download_all(
        message=callback.message,
        url=url,
        novolume=no_volume,
        audio_mp3=mp3,
        image=image,
        quality=quality


    )


@callback_router.callback_query(lambda c: c.data == '1080p')
async def quality_1080p(callback: CallbackQuery, state: FSMContext):

    await state.update_data(quality=1080)

    update_keyboard = quality_inline_keyboard(quality=1080)

    await callback.message.edit_reply_markup(reply_markup=update_keyboard)

    await callback.answer("Выбрано 1080p")

@callback_router.callback_query(lambda c: c.data == '360p')
async def quality_360p(callback: CallbackQuery, state: FSMContext):

    await state.update_data(quality=360)

    update_keyboard = quality_inline_keyboard(quality=360)

    await callback.message.edit_reply_markup(reply_markup=update_keyboard)

    await callback.answer("Выбрано 360p")

@callback_router.callback_query(lambda c: c.data == '720p')
async def quality_720p(callback: CallbackQuery, state: FSMContext):

    await state.update_data(quality=720)

    update_keyboard = quality_inline_keyboard(quality=720)

    await callback.message.edit_reply_markup(reply_markup=update_keyboard)

    await callback.answer("Выбрано 720p")









@callback_router.callback_query(lambda c: c.data == 'back')
async def back_keyboard(callback: CallbackQuery, state: FSMContext):

    update_keyboard = main_inline_keyboard()

    await callback.message.edit_reply_markup(reply_markup=update_keyboard)
    await callback.answer()


@callback_router.callback_query(lambda c: c.data == 'quality')
async def quality_keyboard(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    current_status = data.get('quality', 360)

    new_status = not current_status

    await state.update_data(quality=new_status)

    update_keyboard = quality_inline_keyboard(quality=new_status)

    await callback.message.edit_reply_markup(reply_markup=update_keyboard)
    await callback.answer()

@callback_router.message(F.text.contains("youtube.com") | F.text.contains("youtu.be") | F.text.contains("tiktok.com") | F.text.contains("pinterest.com") | F.text.contains("pin.it"))
async def handle_link(message: Message, state: FSMContext):

    url = message.text.strip()

    await state.update_data(
        video_url=url,
        no_volume=False,
        mp3=False,
        image=False,
        quality=360
    )

    keyboard = main_inline_keyboard(no_volume=False, mp3=False)
    caption_text = (f"**Сыллка:** {url}\n\n"
                    f"🔧 Настройте свойства медиафайла: "

                    )

    image_dir = os.path.abspath('photo/random_photo')

    chosen_photo = None

    if os.path.exists(image_dir) and os.path.isdir(image_dir):
        valid_extensions = ('.jpg', '.png', '.jpeg')

        all_images = [
            f for f in os.listdir(image_dir)
            if f.lower().endswith(valid_extensions)

        ]

        if all_images:
            random_image = random.choice(all_images)
            chosen_photo = os.path.join(image_dir, random_image)

    if isinstance(url, str):
        url = url.strip("[]'\" ")
    elif isinstance(url, list) and len(url) > 0:
        url = str(url[0]).strip("[]'\" ")

    photo = FSInputFile(chosen_photo)

    await message.answer_photo(photo=photo, caption=caption_text, reply_markup=keyboard)



