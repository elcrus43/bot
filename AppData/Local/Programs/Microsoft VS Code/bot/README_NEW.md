# 🤖 Telegram Bot для Агентства Недвижимости

AI-ассистент для агентства недвижимости в Кирове с интеграцией Groq API и Supabase.

## ✨ Возможности

- 🏠 **Консультации**: Покупка, продажа, аренда недвижимости
- 🤖 **AI-ответы**: Интеграция с Groq Llama 3.3 70B для умных ответов
- 📊 **Сбор лидов**: Автоматический сбор контактов заинтересованных клиентов
- 🔔 **Уведомления**: Мгновенные уведомления риэлтора о новых лидах
- 📈 **Статистика**: Админ-панель со статистикой бота
- 🛡️ **Валидация**: Проверка телефонов и имён пользователей
- ⚡ **Rate Limiting**: Защита от спама
- 📝 **Логирование**: Расширенное логирование с ротацией файлов

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/elcrus43/bot.git
cd bot
```

### 2. Установка зависимостей

```bash
# Создание виртуального окружения (рекомендуется uv)
pip install uv
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Установка зависимостей
uv pip install -r requirements.txt
```

### 3. Настройка переменных окружения

```bash
# Копирование примера
cp .env.example .env

# Редактирование .env
# Заполните своими значениями (см. ниже)
```

### 4. Получение ключей

#### Bot Token
1. Откройте [@BotFather](https://t.me/BotFather)
2. `/newbot` → придумайте имя и username
3. Скопируйте токен в `.env`

#### Supabase
1. Создайте проект на [supabase.com](https://supabase.com)
2. Settings → API → скопируйте URL и Service Role Key
3. Создайте таблицы (см. ниже)

#### Groq API
1. Зарегистрируйтесь на [console.groq.com](https://console.groq.com)
2. API Keys → Create API Key
3. Скопируйте ключ в `.env`

#### Telegram ID
1. Откройте [@userinfobot](https://t.me/userinfobot)
2. Нажмите Start → получите ваш ID
3. Добавьте в `.env` как `REALTOR_TELEGRAM_ID` и `ADMIN_IDS`

### 5. Запуск бота

```bash
# Development
python main_new.py

# Production (с pm2 или systemd)
pm2 start main_new.py --name realty-bot
```

## 📋 Структура проекта

```
bot/
├── main_new.py         # Точка входа
├── handlers_new.py     # Обработчики сообщений
├── ai_new.py           # Groq AI интеграция
├── database_new.py     # Supabase клиент
├── knowledge.md        # База знаний для AI
├── requirements.txt    # Зависимости
├── .env.example        # Пример конфигурации
├── tests/
│   ├── conftest.py     # Фикстуры pytest
│   ├── test_handlers.py # Тесты handlers
│   └── test_validators.py # Тесты валидации
└── logs/               # Логи бота (создаётся автоматически)
```

## 🗄️ База данных (Supabase)

### Таблица: leads

```sql
CREATE TABLE leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  telegram_id BIGINT NOT NULL UNIQUE,
  username TEXT,
  full_name TEXT,
  phone TEXT,
  interest TEXT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_leads_telegram_id ON leads(telegram_id);
CREATE INDEX idx_leads_interest ON leads(interest);
```

### Таблица: messages

```sql
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_lead_id ON messages(lead_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

### RLS Policies (безопасность)

```sql
-- Включить RLS
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Разрешить вставку через сервисный ключ
CREATE POLICY "Service role can do anything on leads" ON leads
  FOR ALL USING (true);

CREATE POLICY "Service role can do anything on messages" ON messages
  FOR ALL USING (true);
```

## 🧪 Тестирование

```bash
# Запуск всех тестов
pytest

# Запуск с подробным выводом
pytest -v

# Запуск с coverage
pytest --cov=handlers_new --cov=ai_new --cov=database_new

# Запуск конкретного теста
pytest tests/test_validators.py -v
```

## 📊 Админ команды

| Команда | Описание |
|---------|----------|
| `/stats` | Статистика бота (лиды, сообщения, интересы) |
| `/health` | Проверка здоровья бота (API, БД, Telegram) |
| `/help` | Справка по возможностям бота |

## 🔧 Конфигурация (.env)

```bash
# Bot Token (обязательно)
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Supabase (обязательно)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key

# Groq API (обязательно)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx

# Telegram ID (обязательно)
REALTOR_TELEGRAM_ID=123456789
ADMIN_IDS=123456789,987654321

# Опционально
MAX_HISTORY_MESSAGES=20
```

## 🆙 Миграция со старой версии

### 1. Резервное копирование
```bash
cp handlers.py handlers_old.py
cp ai.py ai_old.py
cp database.py database_old.py
cp main.py main_old.py
```

### 2. Обновление файлов
```bash
# Копирование новых версий
cp handlers_new.py handlers.py
cp ai_new.py ai.py
cp database_new.py database.py
cp main_new.py main.py
```

### 3. Обновление зависимостей
```bash
pip install -r requirements.txt
# или
uv pip install -r requirements.txt
```

### 4. Добавление переменных окружения
```bash
# Добавить в .env:
ADMIN_IDS=ваш_id
MAX_HISTORY_MESSAGES=20
```

### 5. Перезапуск бота
```bash
# Остановить старого
# Запустить нового
python main.py
```

## 🛠️ Устранение проблем

### Бот не запускается
```bash
# Проверка переменных окружения
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('BOT_TOKEN'))"

# Проверка логов
cat logs/bot.log
```

### Ошибка Groq API
- Проверьте ключ в `.env`
- Проверьте баланс на [console.groq.com](https://console.groq.com)
- Проверьте лимиты API

### Ошибка Supabase
- Проверьте URL и ключ в `.env`
- Проверьте что таблицы созданы
- Проверьте RLS политики

## 📈 Мониторинг

### Логи
```bash
# Просмотр логов в реальном времени
tail -f logs/bot.log

# Последние 100 строк
tail -n 100 logs/bot.log
```

### Метрики
- `/stats` — лиды и сообщения
- `/health` — статус компонентов
- Логи — ошибки и предупреждения

## 🔐 Безопасность

- ✅ Токены в `.env` (не в коде)
- ✅ Валидация пользовательского ввода
- ✅ Rate limiting (защита от спама)
- ✅ Обработка ошибок с логированием
- ✅ RLS в Supabase
- ✅ Retry логика для API

## 📝 License

MIT

## 👥 Контакты

- GitHub: [@elcrus43](https://github.com/elcrus43)
- Проект: bot

---

**Сделано с** ❤️ **для агентства недвижимости в Кирове**
