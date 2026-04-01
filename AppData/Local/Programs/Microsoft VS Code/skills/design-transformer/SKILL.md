---
name: design-transformer
description: |
  Изменяет дизайн сайта: цвета, шрифты, компоновку, стиль.
  Triggers on: "изменить дизайн", "редизайн", "сменить стиль", "redesign", "новый дизайн"
metadata:
  version: 1.0.0
  author: elcrus43
---

# Design Transformer Skill

Трансформация дизайна существующего сайта с сохранением структуры и контента.

## 🎯 Режимы работы

### 1. Быстрый редизайн (1-2 дня)
**Что меняет**:
- Цветовая схема
- Шрифты
- Отступы и размеры
- Скругления углов
- Тени и эффекты

**Что сохраняет**:
- Структуру блоков
- Контент (тексты, фото)
- Расположение элементов

---

### 2. Полный редизайн (1-2 недели)
**Что меняет**:
- Визуальный стиль полностью
- Компоновку блоков
- Анимации и переходы
- Иконки и иллюстрации
- Адаптивность

**Что сохраняет**:
- Контент (тексты, фото)
- Функционал (формы, кнопки)

---

### 3. Частичный редизайн (по запросу)
**Что меняет**:
- Отдельные компоненты (header, footer, карточки)
- Конкретные страницы
- Определённые стили

---

## 🎨 Пресеты дизайна

### Для сайта риэлтора (yelchugin.ru)

#### Пресет 1: "Современный минимализм"

**Характеристики**:
- Много белого пространства
- Крупная типографика
- Минимум декоративных элементов
- Акцент на контенте
- Тонкие линии и границы

**Цветовая палитра**:
```css
:root {
  --background: #ffffff;
  --background-secondary: #f9fafb;
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --primary: #3b82f6;
  --primary-hover: #2563eb;
  --accent: #f59e0b;
  --border: #e5e7eb;
  --success: #10b981;
  --error: #ef4444;
}
```

**Шрифты**:
```css
font-family: 'Inter', sans-serif;
font-size: 16px;
line-height: 1.6;
```

**Пример компонента**:
```tsx
// Карточка услуги в стиле минимализм
<div className="p-8 border border-gray-200 hover:border-blue-500 transition-colors">
  <h3 className="text-xl font-semibold mb-3">Купить квартиру</h3>
  <p className="text-gray-600 mb-4">
    Подберём варианты по вашим критериям...
  </p>
  <a href="#" className="text-blue-600 font-medium hover:underline">
    Подробнее →
  </a>
</div>
```

---

#### Пресет 2: "Премиум"

**Характеристики**:
- Тёмные тона с золотыми акцентами
- Градиенты и тени
- Плавные анимации
- Элегантные шрифты с засечками

**Цветовая палитра**:
```css
:root {
  --background: #0f172a;
  --background-secondary: #1e293b;
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --primary: #fbbf24;
  --primary-hover: #f59e0b;
  --accent: #fbbf24;
  --border: #334155;
  --success: #34d399;
  --error: #f87171;
}
```

**Шрифты**:
```css
/* Заголовки */
font-family: 'Playfair Display', serif;

/* Текст */
font-family: 'Lato', sans-serif;
```

**Пример компонента**:
```tsx
// Карточка услуги в премиум стиле
<div className="relative p-10 bg-gradient-to-br from-slate-900 to-slate-800 rounded-2xl shadow-2xl hover:shadow-amber-500/20 transition-shadow">
  <div className="absolute top-0 right-0 w-32 h-32 bg-amber-500/10 rounded-full blur-3xl" />
  
  <h3 className="text-2xl font-serif text-amber-400 mb-4">
    Купить квартиру
  </h3>
  <p className="text-slate-300 mb-6 leading-relaxed">
    Эксклюзивная подборка лучших предложений...
  </p>
  <button className="px-8 py-3 bg-gradient-to-r from-amber-500 to-amber-600 text-white font-medium rounded-lg hover:from-amber-600 hover:to-amber-700 transition-all">
    Узнать подробнее
  </button>
</div>
```

---

#### Пресет 3: "Дружелюбный"

**Характеристики**:
- Яркие, тёплые цвета
- Скруглённые углы
- Игривые иконки
- Неформальный тон

**Цветовая палитра**:
```css
:root {
  --background: #fefefe;
  --background-secondary: #fff7ed;
  --text-primary: #1f2937;
  --text-secondary: #6b7280;
  --primary: #f97316;
  --primary-hover: #ea580c;
  --accent: #84cc16;
  --border: #fed7aa;
  --success: #22c55e;
  --error: #ef4444;
}
```

**Шрифты**:
```css
font-family: 'Nunito', sans-serif;
border-radius: 16px; /* Скругления везде */
```

---

#### Пресет 4: "Корпоративный"

**Характеристики**:
- Строгие цвета (синий, серый, белый)
- Чёткая сетка
- Минимум анимаций
- Профессиональный вид

**Цветовая палитра**:
```css
:root {
  --background: #ffffff;
  --background-secondary: #f3f4f6;
  --text-primary: #1f2937;
  --text-secondary: #4b5563;
  --primary: #1e40af;
  --primary-hover: #1e3a8a;
  --accent: #059669;
  --border: #d1d5db;
  --success: #059669;
  --error: #dc2626;
}
```

**Шрифты**:
```css
font-family: 'Roboto', sans-serif;
```

---

## 🛠️ Процесс трансформации

### Шаг 1: Анализ текущего дизайна

**Что смотрим**:
```bash
# Текущие цвета
- Primary: #2563eb (синий)
- Secondary: #1e40af (тёмно-синий)
- Accent: #f59e0b (оранжевый)

# Текущие шрифты
- TildaSans или Arial

# Компоненты
- Header: фиксированный, белый
- Hero: фото + форма
- Services: карточки 3 в ряд
- Form: поля с серой рамкой
```

### Шаг 2: Выбор пресета

**Вопросы для выбора**:
1. Кто целевая аудитория?
   - Молодёжь → "Дружелюбный"
   - Бизнес → "Корпоративный"
   - Премиум клиенты → "Премиум"
   - Все → "Минимализм"

2. Какой образ хотите создать?
   - Доступный → "Дружелюбный"
   - Профессиональный → "Корпоративный"
   - Элитный → "Премиум"

3. Какой текущий стиль?
   - Устаревший → "Минимализм"
   - Слишком яркий → "Корпоративный"
   - Скучный → "Премиум" или "Дружелюбный"

### Шаг 3: Применение нового дизайна

#### Глобальные изменения

**tailwind.config.js**:
```js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#3b82f6',
          hover: '#2563eb',
        },
        secondary: {
          DEFAULT: '#f9fafb',
        },
        accent: {
          DEFAULT: '#f59e0b',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        heading: ['Inter', 'sans-serif'],
      },
      borderRadius: {
        DEFAULT: '8px',
        lg: '12px',
        xl: '16px',
      },
    },
  },
}
```

#### Обновление компонентов

**До (старый дизайн)**:
```tsx
<button className="px-6 py-3 bg-blue-600 text-white rounded">
  Отправить
</button>
```

**После (минимализм)**:
```tsx
<button className="px-8 py-4 bg-blue-500 text-white font-medium rounded-lg hover:bg-blue-600 transition-colors shadow-sm">
  Отправить
</button>
```

**После (премиум)**:
```tsx
<button className="px-10 py-5 bg-gradient-to-r from-amber-500 to-amber-600 text-white font-semibold rounded-xl hover:from-amber-600 hover:to-amber-700 transition-all shadow-lg hover:shadow-amber-500/30">
  Отправить
</button>
```

---

### Шаг 4: Тестирование

**Чеклист**:
- [ ] Все страницы выглядят хорошо
- [ ] Мобильная версия работает
- [ ] Кнопки кликабельны
- [ ] Формы работают
- [ ] Контраст цветов соответствует WCAG
- [ ] Анимации не тормозят

---

## 📊 Примеры трансформаций

### Пример 1: Tilda → Современный минимализм

**До**:
- Яркие градиенты
- Тени везде
- Мелкие отступы
- Разные шрифты

**После**:
- Белый фон
- Один шрифт (Inter)
- Большие отступы
- Минимум декора

**Изменения в коде**:
```diff
- <div class="t-section" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
+ <section className="py-20 bg-white">

- <h2 style="font-size: 48px; font-weight: 900; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
+ <h2 className="text-4xl font-bold text-gray-900">

- <button style="border-radius: 50px; box-shadow: 0 10px 20px rgba(0,0,0,0.3);">
+ <button className="px-8 py-4 bg-blue-500 text-white rounded-lg shadow-sm">
```

---

### Пример 2: Корпоративный → Дружелюбный

**До**:
- Синий #1e40af
- Строгие линии
- Нет скруглений

**После**:
- Оранжевый #f97316
- Скругления 16px
- Тёплые иконки

**Изменения**:
```diff
- colors: { primary: '#1e40af' }
+ colors: { primary: '#f97316' }

- borderRadius: '0px'
+ borderRadius: '16px'

- <BuildingIcon className="w-12 h-12 text-blue-900" />
+ <BuildingIcon className="w-12 h-12 text-orange-500" />
```

---

## 🎯 Быстрые команды

```bash
# Применить пресет
/design-transformer --preset modern-minimal ./src

# Изменить только цвета
/design-transformer --colors-only --palette warm ./src

# Изменить только шрифты
/design-transformer --fonts-only --font inter ./src

# Полный редизайн
/design-transformer --preset premium --full ./src

# Частичный (только header)
/design-transformer --components header,footer ./src
```

---

## 📁 Формат вывода

```json
{
  "preset": "modern-minimal",
  "changes": {
    "colors": {
      "primary": "#3b82f6",
      "secondary": "#f9fafb",
      "accent": "#f59e0b"
    },
    "fonts": {
      "sans": "Inter",
      "heading": "Inter"
    },
    "borderRadius": "8px",
    "animations": "minimal"
  },
  "filesChanged": [
    "tailwind.config.js",
    "src/styles/globals.css",
    "src/components/sections/Header.tsx",
    "src/components/sections/Hero.tsx",
    "src/components/sections/Services.tsx"
  ],
  "estimatedTime": "2-3 часа"
}
```

---

## Examples

**Триггеры для активации**:
- "сделай редизайн сайта"
- "измени дизайн на современный"
- "хочу премиум стиль"
- "поменяй цвета на синие"
- "redesign website"
- "change color scheme"
