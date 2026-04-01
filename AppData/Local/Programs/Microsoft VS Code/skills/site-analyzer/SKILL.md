---
name: site-analyzer
description: |
  Анализирует структуру, технологии и архитектуру сайта.
  Triggers on: "анализ сайта", "разобрать сайт", "какие технологии", "site analysis", "анализировать yelchugin.ru"
metadata:
  version: 1.0.0
  author: elcrus43
---

# Site Analyzer Skill

Анализирует веб-сайт и определяет технологии, структуру и архитектуру.

## 🎯 Что определяет

### Технические характеристики
- **Фреймворк/CMS**: React, Vue, Angular, Next.js, Tilda, WordPress, etc.
- **CSS**: Tailwind, Bootstrap, styled-components, чистый CSS
- **State Management**: Redux, Zustand, Vuex (если SPA)
- **API**: REST, GraphQL, tRPC
- **Хостинг**: Vercel, Netlify, AWS, Timeweb
- **Аналитика**: Google Analytics, Yandex Metrika, Pixel

### Структура
- **Тип**: Лендинг, многостраничный, SPA, PWA
- **Компоненты**: Header, Footer, Hero, Features, Forms, Cards
- **Контент**: Текст, изображения, видео, формы

### Дизайн
- **Цветовая схема**: Основные цвета, акценты, градиенты
- **Типографика**: Шрифты, размеры, иерархия
- **Стиль**: Минимализм, корпоративный, современный

## 🛠️ Процесс анализа

### Шаг 1: Сканирование URL
```bash
# Получение HTML
curl -s https://yelchugin.ru | head -100

# Анализ заголовков
curl -I https://yelchugin.ru
```

### Шаг 2: Определение технологий

**Ищем маркеры в HTML**:
```html
<!-- Tilda -->
<link rel="stylesheet" href="https://static.tildacdn.com/...">
<script src="https://static.tildacdn.com/js/..."></script>

<!-- WordPress -->
<link rel="https://api.w.org/" ...>
<meta name="generator" content="WordPress 6.x">

<!-- React -->
<div id="root"></div>
<script src="/static/js/main.[hash].js"></script>

<!-- Tailwind CSS -->
<div class="flex items-center justify-center">

<!-- Bootstrap -->
<div class="container-fluid">
<link rel="stylesheet" href="bootstrap.min.css">
```

### Шаг 3: Анализ структуры

**Дерево страницы**:
```
Homepage
├── Header
│   ├── Logo
│   ├── Navigation (Купить, Продать, Сдать, Ипотека, Новостройки, Сервис)
│   └── Contact Button
├── Hero Section
│   ├── Title
│   ├── Subtitle
│   └── CTA Form
├── About Section
│   ├── Photo
│   ├── Name & Title
│   └── Experience Stats
├── Services Section
│   ├── Service Cards (8-12 items)
│   └── Icons
├── Process Section
│   ├── Steps (4 этапа)
│   └── Timeline
├── Benefits Section
│   ├── List of Advantages
│   └── Icons
├── Lead Form Section
│   ├── Service Selector
│   ├── Input Fields (Name, Phone)
│   └── Submit Button
├── Referral Program
│   ├── Conditions
│   └── Reward Info (5000 ₽)
├── Contact Section
│   ├── Address (г. Киров)
│   ├── Working Hours
│   └── Phone/Email
└── Footer
    ├── Copyright
    └── "Конструктор сайтов"
```

### Шаг 4: Извлечение цветов

**Палитра**:
```css
/* Пример для сайта недвижимости */
--primary-color: #2563eb;      /* Синий - доверие */
--secondary-color: #1e40af;    /* Тёмно-синий */
--accent-color: #f59e0b;       /* Оранжевый - CTA */
--background: #ffffff;         /* Белый фон */
--text-primary: #1f2937;       /* Тёмно-серый текст */
--text-secondary: #6b7280;     /* Светло-серый */
--success: #10b981;            /* Зелёный */
--error: #ef4444;              /* Красный */
```

### Шаг 5: Анализ шрифтов

**Типографика**:
```css
/* Подключаемые шрифты */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Или Tilda стандарт */
font-family: 'TildaSans', Arial, sans-serif;
font-size: 16px;
line-height: 1.5;
```

## 📋 Вывод анализа

### Для yelchugin.ru (пример)

**Технологии**:
- **Платформа**: Tilda Publishing (конструктор)
- **CSS**: Tilda встроенные стили + кастомные
- **JS**: jQuery + Tilda scripts
- **Формы**: Tilda Forms
- **Хостинг**: Tilda CDN
- **Аналитика**: Yandex Metrika (вероятно)

**Структура**:
- **Тип**: Лендинг с якорными ссылками
- **Блоков**: 9 основных секций
- **Форм**: 1 основная форма захвата
- **Страниц**: 1 (возможно есть отдельные через Tilda)

**Дизайн**:
- **Стиль**: Корпоративный минимализм
- **Цвета**: Синий (доверие), белый (чистота), оранжевый (акцент)
- **Шрифты**: TildaSans или аналог (гротеск)
- **Адаптивность**: Есть (Tilda автоматически)

**Контент**:
- **Тон**: Профессиональный, доверительный
- **ЦА**: Покупатели/продавцы недвижимости в Кирове
- **УТП**: Опыт, юридическая защита, оплата за результат

## 🔄 Рекомендации по миграции

### Если переносим с Tilda на Next.js:

**Преимущества**:
- ✅ Полный контроль над кодом
- ✅ Лучшая производительность
- ✅ SEO оптимизация
- ✅ Масштабируемость
- ✅ Интеграция с CRM

**Сложности**:
- ⚠️ Нужно писать код с нуля
- ⚠️ Хостинг отдельно (Vercel/Netlify)
- ⚠️ Формы через API
- ⚠️ Контент через CMS

**План миграции**:
1. Экспорт контента из Tilda
2. Создание Next.js проекта
3. Конвертация блоков в компоненты
4. Перенос стилей в Tailwind
5. Подключение форм (EmailJS/Supabase)
6. Настройка аналитики
7. Деплой на Vercel

**Время**: 2-4 недели

### Если оставляем на Tilda:

**Улучшения**:
- ✅ Добавить больше страниц (отдельно под каждую услугу)
- ✅ Настроить SEO (meta tags, sitemap)
- ✅ Добавить отзывы клиентов
- ✅ Кейсы с фото "до/после"
- ✅ Калькулятор ипотеки
- ✅ Чат-бот для консультаций

## 📊 Метрики качества

**Хороший сайт недвижимости**:
- ✅ Загрузка < 3 секунд
- ✅ Мобильная версия 100% рабочая
- ✅ Формы работают
- ✅ Контакты кликабельны (tel:, mailto:)
- ✅ Аналитика подключена
- ✅ SEO оптимизирован
- ✅ SSL сертификат есть

## 🎯 Примеры команд

```bash
# Анализ конкретного сайта
/site-analyzer https://yelchugin.ru

# Анализ с рекомендациями
/site-analyzer https://yelchugin.ru --recommendations

# Сравнение с конкурентами
/site-analyzer https://yelchugin.ru --compare https://competitor1.ru,https://competitor2.ru

# Экспорт структуры
/site-analyzer https://yelchugin.ru --export structure.json
```

## 📁 Формат вывода

```json
{
  "url": "https://yelchugin.ru",
  "platform": "Tilda",
  "type": "landing",
  "blocks": [
    "header",
    "hero",
    "about",
    "services",
    "process",
    "benefits",
    "form",
    "referral",
    "contacts",
    "footer"
  ],
  "colors": {
    "primary": "#2563eb",
    "secondary": "#1e40af",
    "accent": "#f59e0b"
  },
  "fonts": ["TildaSans", "Arial"],
  "forms": 1,
  "mobile_ready": true,
  "recommendations": [
    "Добавить страницу услуг",
    "Настроить SEO",
    "Добавить отзывы"
  ]
}
```

---

## Examples

**Триггеры для активации**:
- "проанализируй сайт yelchugin.ru"
- "какие технологии на сайте"
- "разбери структуру сайта"
- "site analysis"
- "хочу перенести сайт на другую платформу"
