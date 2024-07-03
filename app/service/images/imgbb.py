import asyncio
import base64

import aiohttp

from app import settings


async def imgbb__upload_photo(tg_link: str):
    """загрузка картинки на imgbb"""
    async with aiohttp.ClientSession() as session:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": settings.IMGBB_KEY,
            "image": tg_link,
        }
        response = await session.post(url, params=payload)
        if response.status == 200:
            resp_json = await response.json()
            return resp_json["data"]["url"]
    return None
