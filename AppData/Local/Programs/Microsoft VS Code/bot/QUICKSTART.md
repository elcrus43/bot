# 🚀 Быстрый старт

## 1. Заполните .env

Откройте `.env` и заполните переменные:

```bash
# Bot Token (получить в @BotFather)
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Supabase (получить в https://supabase.com)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key

# Groq API (получить в https://console.groq.com)
GROQ_API_KEY=gsk_xxxxxxxxxxxx

# Telegram ID (получить в @userinfobot)
REALTOR_TELEGRAM_ID=123456789
ADMIN_IDS=123456789
```

## 2. Проверьте конфигурацию

```bash
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('BOT_TOKEN:', 'OK' if os.getenv('BOT_TOKEN') else 'MISSING')"
```

## 3. Запустите бота

```bash
python main.py
```

## 4. Проверьте в Telegram

1. Откройте вашего бота
2. Нажмите `/start`
3. Бот должен ответить приветствием

## 5. Проверьте админ команды

Если ваш ID добавлен в `ADMIN_IDS`:

```
/stats  — статистика бота
/health — проверка здоровья
```

## 6. Логи

Логи сохраняются в `logs/bot.log`

```bash
# Просмотр в реальном времени
tail -f logs/bot.log
```

## 🆘 Проблемы?

### Бот не запускается
```bash
# Проверьте переменные окружения
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('BOT_TOKEN'))"

# Проверьте логи
cat logs/bot.log
```

### Ошибка токена
- Проверьте токен в @BotFather
- Убедитесь что нет лишних пробелов в .env

### Ошибка Supabase
- Проверьте URL и ключ в настройках проекта Supabase
- Убедитесь что таблицы созданы (см. README_NEW.md)

### Ошибка Groq
- Проверьте ключ в https://console.groq.com
- Проверьте баланс API

---

**Готово!** 🎉 Бот работает с новыми улучшениями!
