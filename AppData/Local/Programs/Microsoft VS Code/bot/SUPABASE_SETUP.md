# 🗄️ Настройка Supabase

## ✅ Данные для подключения

**URL проекта**: https://dgxzkcybwwonqqkisltl.supabase.co  
**Публичный ключ**: `sb_publishable_UT8ghql_EoUoxogSM06K7A_shMG1mE5`  
**Пароль**: `T!2K.B25BYdB$9H`

---

## 📋 Шаг 1: Создание таблиц

### Вариант A: Через SQL Editor (рекомендуется)

1. Откройте [Supabase SQL Editor](https://dgxzkcybwwonqqkisltl.supabase.co/project/_sql)
2. Скопируйте содержимое файла `supabase_setup.sql`
3. Вставьте в SQL Editor
4. Нажмите **Run**
5. Проверьте что таблицы созданы

### Вариант B: Через Table Editor

1. Откройте [Table Editor](https://dgxzkcybwwonqqkisltl.supabase.co/project/editor)
2. Создайте таблицу **leads**:

| Column | Type | Default | Extra |
|--------|------|---------|-------|
| id | uuid | gen_random_uuid() | primary key |
| telegram_id | int8 | - | unique |
| username | text | - | - |
| full_name | text | - | - |
| phone | text | - | - |
| interest | text | - | - |
| notes | text | - | - |
| created_at | timestamptz | now() | - |
| updated_at | timestamptz | now() | - |

3. Создайте таблицу **messages**:

| Column | Type | Default | Extra |
|--------|------|---------|-------|
| id | uuid | gen_random_uuid() | primary key |
| lead_id | uuid | - | foreign key → leads.id |
| role | text | - | check: user/assistant |
| content | text | - | - |
| created_at | timestamptz | now() | - |

---

## 🔑 Шаг 2: Получение Service Role Key

**Важно**: Для работы бота нужен именно **Service Role Key**, а не Public/Anon key!

1. Откройте [API Settings](https://dgxzkcybwwonqqkisltl.supabase.co/project/settings/api)
2. Найдите секцию **Project API keys**
3. Скопируйте **service_role key** (НЕ anon public!)
4. Вставьте в `.env`:

```bash
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 🔐 Шаг 3: Настройка RLS (Row Level Security)

### Включаем RLS

1. Откройте [Authentication → Policies](https://dgxzkcybwwonqqkisltl.supabase.co/project/auth/policies)
2. Для таблицы **leads**:
   - New Policy → Create from scratch
   - Policy name: `Service role full access`
   - Allowed operation: ALL
   - Target roles: service_role
   - Policy definition: `true`
   - Save

3. Для таблицы **messages**:
   - То же самое

### Или через SQL:

```sql
-- Включить RLS
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Политика для service_role
CREATE POLICY "Service role full access" ON leads
  FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE POLICY "Service role full access" ON messages
  FOR ALL TO service_role USING (true) WITH CHECK (true);
```

---

## ✅ Шаг 4: Проверка подключения

### Тест через Python

```python
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(url, key)

# Проверка подключения
response = supabase.table("leads").select("*").execute()
print(f"Connected! Tables: {len(response.data)} leads")
```

### Тест через Dashboard

1. Откройте [Table Editor](https://dgxzkcybwwonqqkisltl.supabase.co/project/editor)
2. Выберите таблицу **leads**
3. Нажмите **Insert** → добавьте тестовую строку
4. Проверьте что данные сохранились

---

## 📊 Шаг 5: Мониторинг

### Просмотр данных

- [Table Editor](https://dgxzkcybwwonqqkisltl.supabase.co/project/editor) — просмотр всех таблиц
- [SQL Editor](https://dgxzkcybwwonqqkisltl.supabase.co/project/_sql) — SQL запросы

### Примеры запросов:

```sql
-- Все лиды
SELECT * FROM leads ORDER BY created_at DESC;

-- Лиды за сегодня
SELECT * FROM leads WHERE created_at >= NOW() - INTERVAL '24 hours';

-- Сообщения для лида
SELECT m.*, l.full_name 
FROM messages m 
JOIN leads l ON m.lead_id = l.id 
ORDER BY m.created_at DESC;

-- Статистика по интересам
SELECT interest, COUNT(*) as count 
FROM leads 
WHERE interest IS NOT NULL 
GROUP BY interest;
```

---

## 🔧 .env файл

После настройки ваш `.env` должен выглядеть так:

```bash
# Bot Token
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Supabase
SUPABASE_URL=https://dgxzkcybwwonqqkisltl.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# SiliconFlow
SILICONFLOW_API_KEY=...

# Telegram IDs
REALTOR_TELEGRAM_ID=123456789
ADMIN_IDS=123456789
```

---

## ⚠️ Важно!

1. **Не коммитьте `.env`** в git! Файл уже в `.gitignore`
2. **Service Role Key** — секретный, не передавайте никому
3. **RLS политики** — обязательны для безопасности
4. **Бэкапы** — настройте автоматические бэкапы в Supabase

---

## 🆘 Проблемы?

### Ошибка "SUPABASE_KEY должен быть задан"
- Проверьте что `.env` в корне проекта
- Проверьте имя переменной (SUPABASE_SERVICE_KEY)

### Ошибка "relation does not exist"
- Таблицы не созданы — выполните SQL скрипт
- Проверьте в Table Editor

### Ошибка "JWT expired"
- Неверный ключ — используйте service_role, не anon

---

**Готово!** После настройки Supabase можно запускать бота! 🚀
