-- Supabase SQL Script для настройки бота
-- Выполнить в Supabase SQL Editor: https://dgxzkcybwwonqqkisltl.supabase.co

-- ============================================
-- 1. Создаём таблицу leads (лиды/клиенты)
-- ============================================
CREATE TABLE IF NOT EXISTS leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  telegram_id BIGINT NOT NULL UNIQUE,
  username TEXT,
  full_name TEXT,
  phone TEXT,
  interest TEXT,
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Индексы для производительности
CREATE INDEX IF NOT EXISTS idx_leads_telegram_id ON leads(telegram_id);
CREATE INDEX IF NOT EXISTS idx_leads_interest ON leads(interest);
CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads(created_at);

-- ============================================
-- 2. Создаём таблицу messages (сообщения)
-- ============================================
CREATE TABLE IF NOT EXISTS messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Индексы для производительности
CREATE INDEX IF NOT EXISTS idx_messages_lead_id ON messages(lead_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);

-- ============================================
-- 3. Включаем Row Level Security (RLS)
-- ============================================
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- ============================================
-- 4. Создаём политики доступа
-- ============================================

-- Политика для leads: сервисный ключ может всё
CREATE POLICY "Service role can do anything on leads" ON leads
  FOR ALL
  USING (true)
  WITH CHECK (true);

-- Политика для messages: сервисный ключ может всё
CREATE POLICY "Service role can do anything on messages" ON messages
  FOR ALL
  USING (true)
  WITH CHECK (true);

-- ============================================
-- 5. Создаём функцию для авто-обновления updated_at
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- 6. Создаём триггер для авто-обновления
-- ============================================
CREATE TRIGGER update_leads_updated_at
  BEFORE UPDATE ON leads
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 7. Проверка создания таблиц
-- ============================================
-- Должно показать 2 строки
SELECT COUNT(*) as table_count FROM information_schema.tables 
WHERE table_schema = 'public' AND table_name IN ('leads', 'messages');

-- ============================================
-- 8. Тестовые данные (опционально, для проверки)
-- ============================================
-- INSERT INTO leads (telegram_id, username, full_name, interest) 
-- VALUES (123456789, 'testuser', 'Test User', 'купить');

-- SELECT * FROM leads;
