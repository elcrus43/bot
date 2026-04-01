import asyncio
from aiogram import Bot
from dotenv import load_dotenv
import os

load_dotenv()

async def test_bot():
    """Тест подключения к Telegram Bot API."""
    token = os.getenv("BOT_TOKEN")
    
    print("🔍 Тестирование Telegram Bot API...\n")
    
    try:
        bot = Bot(token=token)
        
        # Получение информации о боте
        me = await bot.get_me()
        
        print(f"✅ Бот найден!")
        print(f"   ID: {me.id}")
        print(f"   Username: @{me.username}")
        print(f"   Имя: {me.first_name}")
        print(f"   Может читать группы: {me.can_join_groups}")
        print(f"   Режим инкогнито: {me.is_premium}")
        print()
        
        # Проверка что токен валиден
        print("✅ Токен валиден!")
        
        await bot.session.close()
        print("\n✅ Все тесты пройдены! Бот готов к запуску!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("\nПроверьте токен в @BotFather")

if __name__ == "__main__":
    asyncio.run(test_bot())
