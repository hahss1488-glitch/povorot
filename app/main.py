import asyncio
import logging

from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import AsyncEngine

from app.bot.handlers.game import router
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine


async def init_db(db_engine: AsyncEngine) -> None:
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main() -> None:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level)
    await init_db(engine)
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
