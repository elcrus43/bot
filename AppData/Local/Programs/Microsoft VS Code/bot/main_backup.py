import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from handlers import router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def main():
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        logger.error("BOT_TOKEN not found in environment variables!")
        return
    bot = Bot(token=bot_token)
    dp = Dispatcher(storage=MemoryStorage())
    # Регистрация роутеров
    dp.include_router(router)
    # Запуск бота
    logger.info("Bot is starting...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"Bot stopped with error: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
