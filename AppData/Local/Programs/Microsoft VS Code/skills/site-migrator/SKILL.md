---
name: site-migrator
description: |
  Переносит сайт с одной платформы на другую (Tilda → Next.js, WordPress → Astro, etc.).
  Triggers on: "перенести сайт", "миграция сайта", "сменить платформу", "site migration", "перенести yelchugin.ru"
metadata:
  version: 1.0.0
  author: elcrus43
---

# Site Migrator Skill

Помощь в переносе сайтов между платформами с сохранением контента, дизайна и функциональности.

## 🎯 Поддерживаемые миграции

### Популярные направления

| Откуда | Куда | Сложность | Время |
|--------|------|-----------|-------|
| **Tilda** | Next.js + Tailwind | ⭐⭐⭐ | 2-4 недели |
| **Tilda** | Astro | ⭐⭐ | 1-2 недели |
| **WordPress** | Next.js | ⭐⭐⭐⭐ | 3-5 недель |
| **WordPress** | Astro | ⭐⭐⭐ | 2-3 недели |
| **Webflow** | React/Vue | ⭐⭐⭐ | 2-4 недели |
| **HTML** | React компоненты | ⭐⭐ | 1-2 недели |
| **Bootstrap** | Tailwind CSS | ⭐⭐ | 1 неделя |

## 📋 Процесс миграции

### Этап 1: Аудит текущего сайта

**Что анализируем**:
```bash
# 1. Структура страниц
- Главная
- Услуги (список)
- О компании
- Контакты
- Блог (если есть)

# 2. Контент
- Тексты (объём, структура)
- Изображения (количество, размеры)
- Видео (хостинг, интеграции)
- Документы (PDF, прайсы)

# 3. Функционал
- Формы захвата
- Калькуляторы
- Фильтры/поиск
- Интеграции (CRM, email, SMS)
- Аналитика

# 4. SEO
- Meta tags (title, description)
- H1-H6 иерархия
- Sitemap.xml
- Robots.txt
- Redirects (301)
```

**Чеклист аудита**:
- [ ] Количество страниц
- [ ] Количество изображений
- [ ] Формы и их поля
- [ ] Интеграции со сторонними сервисами
- [ ] Текущая аналитика (метрики, цели)
- [ ] SEO настройки
- [ ] Домен и почта

---

### Этап 2: Выбор целевой платформы

#### Для yelchugin.ru (сайт риэлтора)

**Рекомендация**: Next.js + Tailwind CSS + Supabase

**Почему**:
- ✅ Быстрая загрузка (SEO)
- ✅ Легко масштабировать
- ✅ Интеграция с CRM через API
- ✅ Формы на Supabase (сбор лидов)
- ✅ Хостинг на Vercel (бесплатно для старта)
- ✅ Полный контроль над кодом

**Альтернативы**:
- **Astro** — если нужен статический сайт (дешевле хостинг)
- **WordPress** — если нужно часто менять контент без разработчика
- **Tilda** — если нет разработчика и нужно быстро

---

### Этап 3: Создание структуры проекта

#### Next.js структура для сайта риэлтора

```
yelchugin-next/
├── src/
│   ├── app/                    # Next.js 14 App Router
│   │   ├── layout.tsx          # Общий layout
│   │   ├── page.tsx            # Главная
│   │   ├── services/
│   │   │   └── page.tsx        # Услуги
│   │   ├── about/
│   │   │   └── page.tsx        # О себе
│   │   ├── contacts/
│   │   │   └── page.tsx        # Контакты
│   │   └── blog/
│   │       ├── page.tsx        # Блог
│   │       └── [slug]/
│   │           └── page.tsx    # Отдельная статья
│   │
│   ├── components/
│   │   ├── ui/                 # Базовые компоненты
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Card.tsx
│   │   │   └── Modal.tsx
│   │   │
│   │   ├── sections/           # Секции сайта
│   │   │   ├── Header.tsx
│   │   │   ├── Hero.tsx
│   │   │   ├── About.tsx
│   │   │   ├── Services.tsx
│   │   │   ├── Process.tsx
│   │   │   ├── Benefits.tsx
│   │   │   ├── ContactForm.tsx
│   │   │   ├── Referral.tsx
│   │   │   ├── Contacts.tsx
│   │   │   └── Footer.tsx
│   │   │
│   │   └── icons/              # SVG иконки
│   │       ├── PhoneIcon.tsx
│   │       ├── EmailIcon.tsx
│   │       └── LocationIcon.tsx
│   │
│   ├── lib/
│   │   ├── supabase/           # Supabase клиент
│   │   ├── utils.ts            # Утилиты
│   │   └── constants.ts        # Константы
│   │
│   ├── styles/
│   │   └── globals.css         # Глобальные стили + Tailwind
│   │
│   └── types/
│       └── index.ts            # TypeScript типы
│
├── public/
│   ├── images/
│   │   ├── hero.jpg
│   │   ├── about.jpg
│   │   └── services/
│   ├── fonts/
│   └── favicon.ico
│
├── .env.local                  # Переменные окружения
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
└── package.json
```

---

### Этап 4: Конвертация контента

#### HTML → JSX конвертер

**Пример конвертации блока из Tilda**:

**До (Tilda HTML)**:
```html
<div class="t-section" id="about">
  <div class="t-container">
    <div class="t-col t-col_8 t-prefix_2">
      <h2 class="t-title">Обо мне</h2>
      <div class="t-text">
        <p>Меня зовут Ельчугин Александр...</p>
        <p>Опыт работы более 10 лет...</p>
      </div>
      <div class="t-stats">
        <div class="t-stat-item">
          <span class="t-stat-number">500+</span>
          <span class="t-stat-label">Сделок</span>
        </div>
      </div>
    </div>
  </div>
</div>
```

**После (React компонент)**:
```tsx
// src/components/sections/About.tsx
import Image from 'next/image'

export function About() {
  return (
    <section id="about" className="py-20 bg-white">
      <div className="container mx-auto px-4">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-8">
            Обо мне
          </h2>
          
          <div className="prose prose-lg mx-auto">
            <p className="text-gray-600">
              Меня зовут Ельчугин Александр...
            </p>
            <p className="text-gray-600">
              Опыт работы более 10 лет...
            </p>
          </div>
          
          <div className="grid grid-cols-3 gap-8 mt-12">
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600">
                500+
              </div>
              <div className="text-gray-500 mt-2">
                Сделок
              </div>
            </div>
            {/* Другие статистки */}
          </div>
        </div>
      </div>
    </section>
  )
}
```

---

### Этап 5: Перенос стилей

#### Tilda CSS → Tailwind CSS

**Таблица соответствий**:

| Tilda Class | Tailwind Class |
|-------------|----------------|
| `.t-container` | `container mx-auto px-4` |
| `.t-col_8` | `col-span-8` или `w-2/3` |
| `.t-prefix_2` | `col-start-3` или `ml-auto` |
| `.t-title` | `text-3xl font-bold` |
| `.t-text` | `prose` (Typography plugin) |
| `.t-btn` | `px-6 py-3 bg-blue-600 text-white rounded` |

**Пример**:

**До (Tilda CSS)**:
```css
.t-section {
  padding: 80px 0;
  background-color: #ffffff;
}

.t-title {
  font-size: 36px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 40px;
  text-align: center;
}

.t-btn {
  display: inline-block;
  padding: 16px 32px;
  background-color: #2563eb;
  color: #ffffff;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s;
}

.t-btn:hover {
  background-color: #1e40af;
  transform: translateY(-2px);
}
```

**После (Tailwind)**:
```tsx
<section className="py-20 bg-white">
  <h2 className="text-3xl font-bold text-gray-900 mb-10 text-center">
    Заголовок
  </h2>
  
  <button className="inline-block px-8 py-4 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-all hover:-translate-y-0.5">
    Кнопка
  </button>
</section>
```

---

### Этап 6: Перенос форм

#### Tilda Forms → Supabase + React Hook Form

**До (Tilda Form)**:
```html
<form class="t-form" action="/submit" method="post">
  <input type="text" name="name" placeholder="Ваше имя" required>
  <input type="tel" name="phone" placeholder="Телефон" required>
  <select name="service">
    <option value="buy">Купить</option>
    <option value="sell">Продать</option>
  </select>
  <button type="submit">Отправить</button>
</form>
```

**После (React + Supabase)**:
```tsx
// src/components/sections/ContactForm.tsx
import { useState } from 'react'
import { supabase } from '@/lib/supabase'

export function ContactForm() {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    service: 'buy'
  })
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setStatus('loading')
    
    const { error } = await supabase
      .from('leads')
      .insert({
        name: formData.name,
        phone: formData.phone,
        service: formData.service,
        source: 'website'
      })
    
    if (error) {
      setStatus('error')
    } else {
      setStatus('success')
      setFormData({ name: '', phone: '', service: 'buy' })
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        type="text"
        value={formData.name}
        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
        placeholder="Ваше имя"
        required
        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
      />
      
      <input
        type="tel"
        value={formData.phone}
        onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
        placeholder="Телефон"
        required
        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
      />
      
      <select
        value={formData.service}
        onChange={(e) => setFormData({ ...formData, service: e.target.value })}
        className="w-full px-4 py-3 border border-gray-300 rounded-lg"
      >
        <option value="buy">Купить</option>
        <option value="sell">Продать</option>
        <option value="rent">Арендовать</option>
      </select>
      
      <button
        type="submit"
        disabled={status === 'loading'}
        className="w-full px-6 py-4 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:opacity-50"
      >
        {status === 'loading' ? 'Отправка...' : 'Отправить'}
      </button>
      
      {status === 'success' && (
        <p className="text-green-600">✅ Заявка отправлена!</p>
      )}
      {status === 'error' && (
        <p className="text-red-600">❌ Ошибка отправки</p>
      )}
    </form>
  )
}
```

---

### Этап 7: Настройка аналитики

#### Yandex Metrika + Google Analytics

```tsx
// src/app/layout.tsx
import { YandexMetrica } from 'next-yandex-metrica'

export default function RootLayout({ children }) {
  return (
    <html lang="ru">
      <head>
        <YandexMetrica counterId="YOUR_COUNTER_ID" />
        {/* Google Analytics */}
        <script
          async
          src={`https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID`}
        />
        <script
          dangerouslySetInnerHTML={{
            __html: `
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
              gtag('config', 'GA_MEASUREMENT_ID');
            `,
          }}
        />
      </head>
      <body>{children}</body>
    </html>
  )
}
```

**Цели для риэлтора**:
- Отправка формы (лид)
- Клик по телефону
- Клик по WhatsApp
- Просмотр страницы услуги
- Скачивание презентации

---

### Этап 8: Деплой

#### Vercel (рекомендуется для Next.js)

```bash
# 1. Push в GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/elcrus43/yelchugin-next.git
git push -u origin main

# 2. Деплой на Vercel
# Перейти на vercel.com
# Import GitHub Repository
# Выбрать yelchugin-next
# Deploy!

# 3. Настроить домен
# Vercel → Settings → Domains
# Добавить yelchugin.ru
# Настроить DNS у регистратора домена
```

**DNS настройки**:
```
Type: A
Name: @
Value: 76.76.21.21 (Vercel IP)

Type: CNAME
Name: www
Value: cname.vercel-dns.com
```

---

## 📊 Чеклист миграции

### До миграции
- [ ] Полный бэкап текущего сайта
- [ ] Список всех URL (для redirects)
- [ ] Экспорт контента (тексты, изображения)
- [ ] Список интеграций (CRM, email, SMS)
- [ ] Доступы к аналитике
- [ ] Доступы к домену и хостингу

### Во время миграции
- [ ] Создать структуру проекта
- [ ] Конвертировать HTML в компоненты
- [ ] Перенести стили в Tailwind
- [ ] Настроить формы
- [ ] Перенести контент
- [ ] Настроить аналитику
- [ ] Настроить SEO (meta tags, sitemap)

### После миграции
- [ ] Протестировать все страницы
- [ ] Протестировать формы
- [ ] Проверить аналитику
- [ ] Настроить 301 redirects
- [ ] Обновить sitemap.xml
- [ ] Обновить robots.txt
- [ ] Проверить скорость (PageSpeed Insights)
- [ ] Проверить мобильную версию
- [ ] Запустить продакшен

---

## ⏱️ Оценка времени для yelchugin.ru

| Задача | Время |
|--------|-------|
| Аудит текущего сайта | 1 день |
| Создание Next.js проекта | 0.5 дня |
| Конвертация компонентов (9 секций) | 3-4 дня |
| Перенос стилей в Tailwind | 2 дня |
| Настройка форм (Supabase) | 1 день |
| Перенос контента | 1 день |
| Настройка аналитики | 0.5 дня |
| Тестирование | 1-2 дня |
| Деплой и настройка домена | 0.5 дня |
| **Итого** | **10-12 дней** |

---

## 💰 Оценка стоимости (если заказывать)

| Фрилансер | Студия | Сам |
|-----------|--------|-----|
| 50-100 тыс. ₽ | 150-300 тыс. ₽ | Бесплатно (только время) |

---

## Examples

**Триггеры для активации**:
- "перенести сайт с Tilda на Next.js"
- "миграция yelchugin.ru на Astro"
- "хочу сменить платформу сайта"
- "site migration from WordPress"
- "конвертировать HTML в React"
