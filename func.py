import asyncio
import yt_dlp
import gallery_dl
from aiogram.types import Message, FSInputFile, InputMediaPhoto
import re
import os
from pinterest_downloader.pinterest import Pinterest

from be1 import download_tiktok_photo






def download_pinterest(user_id, url: str, image):
    download_dir = os.path.abspath("downloads")
    os.makedirs(download_dir, exist_ok=True)

    try:

        dl = Pinterest()


        res = dl.download_pin(url, path=download_dir)


        if res.get("ok"):
            for file in os.listdir(download_dir):

                if file.endswith((".jpg", ".png")):
                    return os.path.join(download_dir, file)

    except Exception as e:
        print(f"Ошибка pinterest-downloader: {e}")

    return None






def download(user_id: int, url: str, novolume: bool, audio_mp3: bool, image: bool, quality):
    if ("pin.it" in url or "pinterest.com" in url):

        if image:
            return download_pinterest(user_id, url, image)

    if "tiktok.com" in url:
        if image:
            return download_tiktok_photo(user_id, url, image)

    output_format = 'mp3' if audio_mp3 else 'mp4'
    if novolume:
        mya_format = (
            f"bestvideo*[height<={quality}]"
            f"/best[height<={quality}]"
            f"/best"
        )

    elif audio_mp3:
        mya_format = "bestaudio/best"

    else:
        mya_format = (
            f"bestvideo*[height<={quality}]"
            f"+bestaudio/"
            f"best[height<={quality}]"
            f"/best"
        )


    options = {
        'format': mya_format,
        'noplaylist': True,
        'nocheckcert': True,


        "socket_timeout": 150,


        "retries": 3,
        "fragment_retries": 3,


        "source_address": "0.0.0.0"

    }

    if audio_mp3:
        options['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    with yt_dlp.YoutubeDL(options) as ydl:

     info = ydl.extract_info(url, download=False)
     video_title = info.get('title', 'video')
     safe_title = re.sub(r'[\\/*?:"<>|]', "", video_title)

     safe_title = safe_title[:50].strip()

     filename_template = f"{safe_title}.%(ext)s"

     ydl.params.update({
        'outtmpl': {'default': filename_template},
        'merge_output_format': output_format
      })



     if not audio_mp3 and not novolume:
         ydl.params['merge_output_format'] = output_format

     ydl.download([url])

     if audio_mp3:
         return f"{safe_title}.mp3"

     else:
         return f"{safe_title}.mp4"



async def download_all(message: Message, url: str, novolume: bool, audio_mp3: bool, image: bool, quality):

    waiting_msg = await message.answer('Секунду...')

    loop = asyncio.get_event_loop()

    final_filename = None



#-------------------------------------------

    try:
        final_filename = await loop.run_in_executor(None, download, message.chat.id ,url, novolume, audio_mp3, image, quality)
        if not final_filename:
            raise Exception("Файл не был скачан")

        if not quality:
            await message.answer("пж выбери качество")
            return

        if audio_mp3:
            await message.answer_audio(audio=FSInputFile(final_filename))
            return

        elif image:
            files = final_filename if isinstance(final_filename, list) else [final_filename]

            for filename in files:
                if os.path.exists(filename):
                    await message.answer_photo(
                        photo=FSInputFile(filename)
                    )
                    os.remove(filename)

            return


        else:
            await message.answer_video(video=FSInputFile(final_filename))
            return



#------------------------------------------------------------------

    except Exception as err:
        await message.answer(f'Ошибка: {err}')
        return

    finally:
         if isinstance(final_filename, str) and os.path.exists(final_filename):
            os.remove(final_filename)
            print(f'Файл "{final_filename}" был удален')
         await waiting_msg.delete()


