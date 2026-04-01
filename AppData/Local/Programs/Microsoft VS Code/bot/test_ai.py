import asyncio
from ai import get_ai_response, check_siliconflow_health

async def test_ai():
    """Тест SiliconFlow API."""
    print("🔍 Тестирование SiliconFlow API...\n")
    
    # Проверка здоровья
    print("1. Проверка доступности API...")
    health = await check_siliconflow_health()
    print(f"   Статус: {'✅ OK' if health else '❌ ERROR'}\n")
    
    if not health:
        print("API недоступен! Проверьте ключ и интернет.")
        return
    
    # Тест ответа
    print("2. Тест генерации ответа...")
    response = await get_ai_response("Привет! Как дела?", [])
    print(f"   Ответ: {response[:150]}...\n")
    
    # Тест с контекстом
    print("3. Тест с историей диалога...")
    history = [
        {"role": "user", "content": "Какой район лучше для семьи?"},
        {"role": "assistant", "content": "Для семьи рекомендую районы с развитой инфраструктурой..."}
    ]
    response = await get_ai_response("А какая там цена?", history)
    print(f"   Ответ: {response[:150]}...\n")
    
    print("✅ Все тесты пройдены!")

if __name__ == "__main__":
    asyncio.run(test_ai())
