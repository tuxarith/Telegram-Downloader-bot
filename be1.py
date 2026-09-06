import os
import subprocess

def download_tiktok_photo(user_id: int, url: str, image: bool):

        download_dir = os.path.abspath(
            os.path.join("downloads", "tiktok", str(user_id))
        )
        os.makedirs(download_dir, exist_ok=True)

        result = subprocess.run(
            [
                "gallery-dl",
                "--destination",
                download_dir,
                url
            ],
            capture_output=False,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            raise Exception(result.stderr.strip() or "gallery-dl ошибка")

        files = []

        for root, dirs, filenames in os.walk(download_dir):
            for filename in filenames:
                if filename.lower().endswith(
                        (".jpg", ".jpeg", ".png", ".webp")
                ):
                    files.append(
                        os.path.join(root, filename)
                    )

        if not files:
            raise Exception("Фото не найдены")

        files.sort()
        return files





