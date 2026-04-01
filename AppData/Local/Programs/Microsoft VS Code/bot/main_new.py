import asyncio
import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import TelegramUnauthorizedError
from dotenv import load_dotenv
from handlers_new import router

# Настройка логирования с ротацией
def setup_logging():
    """Настройка расширенного логирования с ротацией файлов."""
    log_path = Path(__file__).parent / "logs" / "bot.log"
    log_path.parent.mkdir(exist_ok=True, parents=True)
    
    # Ротация: 10MB, 5 файлов
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Формат
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    logger = logging.getLogger(__name__)
    logger.info("Logging initialized")
    logger.debug(f"Log file: {log_path}")
    
    return logger


async def main():
    load_dotenv()
    logger = setup_logging()
    
    # Проверка токена бота
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        logger.error("BOT_TOKEN not found in environment variables!")
        return
    
    # Инициализация бота с проверкой токена
    try:
        bot = Bot(token=bot_token)
        # Проверка токена через get_me
        bot_info = await bot.get_me()
        logger.info(f"Bot initialized: @{bot_info.username} ({bot_info.first_name})")
    except TelegramUnauthorizedError:
        logger.error("Invalid BOT_TOKEN! Please check your token in @BotFather")
        return
    except Exception as e:
        logger.exception(f"Failed to initialize bot: {e}")
        return
    
    # Инициализация Dispatcher
    dp = Dispatcher(storage=MemoryStorage())
    
    # Регистрация роутеров
    dp.include_router(router)
    
    # Запуск бота
    logger.info("Bot is starting polling...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"Bot stopped with error: {e}")
    finally:
        await bot.session.close()
        logger.info("Bot session closed")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
