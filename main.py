import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.handlers import common
from app.middlewares.db import DbSessionMiddleware
from app.service.db.base import init_db

from app.settings import BOT_TOKEN, DATABASE_URL
from app.handlers import admin, user

logging.basicConfig(level=logging.INFO)

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(storage=MemoryStorage())

    dp.update.middleware(DbSessionMiddleware(session_pool=SessionLocal))

    dp.include_router(admin.router)
    dp.include_router(user.router)
    dp.include_router(common.router)

    # database initialization and tables creation
    await init_db()

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
