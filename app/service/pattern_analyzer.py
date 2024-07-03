from typing import Union, List, Optional

from aiogram.types import Message

from app import settings
from app.service.images.imgbb import imgbb__upload_photo

PHOTO_LINK_BASE: str = "https://api.telegram.org/file/bot{}/{}"


async def analyze_recipe(message: Message) -> Union[List, dict]:
    """анализ паттернов в сообщении и возврат данных для занесения в базу"""
    text: str = message.html_text
    errors: List[str] = []

    if len(text.split("\n")) == 1:
        errors.append("Рецепцт не может состоять только из заголовка!")

    if len(text) < 80:
        errors.append("Слишком маленький рецепт, напишите подробнее!")

    title: str = text.split("\n")[0]
    if len(title) > 40:
        errors.append("Заголовок (1 строка) должен быть не более 40 символов.")

    description: str = "\n".join(text.split("\n")[1:])

    photo_uri: Optional[str] = None
    if message.photo:
        file_id = message.photo[-1].file_id
        file = await message.bot.get_file(file_id=file_id)
        photo_uri = PHOTO_LINK_BASE.format(
            settings.BOT_TOKEN, file.file_path
        )

    if errors:
        return errors

    return {
        "title": title,
        "description": description,
        "media_uri": await imgbb__upload_photo(photo_uri) if photo_uri else None,
        "user": message.chat.id,
    }


