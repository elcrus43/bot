---
name: ui-ux-designer
description: |
  Профессиональный UI/UX дизайн: дизайн-системы, генерация интерфейсов, best practices.
  Triggers on: "дизайн сайта", "ui ux", "создать интерфейс", "design system", "редизайн"
metadata:
  version: 1.0.0
  author: elcrus43 (adapted from UI/UX Pro Max Skill)
---

# UI/UX Designer Skill

Профессиональный дизайн-интеллект для создания UI/UX на множестве платформ. Адаптировано из [UI/UX Pro Max Skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill).

## 🎯 Возможности

### 1. Интеллектуальная генерация дизайн-систем

**Что создаёт**:
- **Паттерн**: Минимализм, Премиум, Корпоративный, Дружелюбный
- **Стиль**: 67 отраслевых стилей
- **Палитра**: 161 цветовая схема
- **Типографика**: 57 шрифтовых пар
- **Эффекты**: Тени, градиенты, анимации
- **Компоненты**: Кнопки, карточки, формы, навигация

**Процесс**:
```
1. Запрос пользователя → "Создай лендинг для риэлтора"
2. Анализ требований → ЦА, стиль, функционал
3. Применение 161 правила UX
4. Генерация дизайн-системы
5. Создание макета в коде
6. Предварительная проверка
```

---

### 2. Поддерживаемые платформы

**Фреймворки**:
- React + Tailwind CSS (по умолчанию)
- Next.js 14 App Router
- Vue 3 + Nuxt
- Svelte + SvelteKit
- Astro
- Angular
- Laravel + Blade
- HTML + Tailwind (статический)

**Мобильные**:
- React Native
- Flutter
- SwiftUI (iOS)
- Jetpack Compose (Android)

**UI библиотеки**:
- shadcn/ui
- Material UI
- Chakra UI
- Ant Design
- Radix UI

---

### 3. База знаний

**Стили дизайна (67)**:
```
Минимализм, Премиум, Корпоративный, Дружелюбный,
Игривый, Элегантный, Современный, Классический,
Технологичный, Природный, Городской, Винтажный,
Ар-деко, Баухаус, Материал, Неоморфизм,
Глассморфизм, Брутализм, Ретро, Футуристичный...
```

**Цветовые палитры (161)**:
```
Океанский бриз, Закат в горах, Северное сияние,
Корпоративный синий, Эко зелёный, Энергия оранжевый,
Премиум золото, Технологичный фиолетовый...
```

**Шрифтовые пары (57)**:
```
Inter + Inter (универсальная)
Playfair Display + Lato (премиум)
Roboto + Roboto (корпоративный)
Nunito + Nunito (дружелюбный)
Poppins + Open Sans (современный)
Montserrat + Merriweather (элегантный)
```

**UX гайдлайны (99)**:
```
Правило 3 кликов
Закон Фиттса
Закон Хика
Принцип близости
Контраст и доступность (WCAG 2.1)
Мобильная-first адаптивность
Согласованность интерфейса
Визуальная иерархия
```

---

## 🎨 Генерация дизайн-системы

### Для сайта риэлтора (yelchugin.ru)

**Анализ требований**:
```
Продукт: Сайт риэлтора
ЦА: Покупатели/продавцы недвижимости 25-65 лет
Стиль: Профессиональный, доверительный
Платформа: Next.js + Tailwind CSS
```

**Генерация**:

#### 1. Выбор стиля

**Рекомендация**: "Современный минимализм"

**Почему**:
- Вызывает доверие
- Акцент на контенте
- Быстрая загрузка
- Универсально для ЦА 25-65 лет

#### 2. Цветовая палитра

**Основная**:
```css
:root {
  /* Primary - Доверие, профессионализм */
  --primary: #2563eb;        /* Синий */
  --primary-hover: #1e40af;  /* Тёмно-синий */
  --primary-light: #dbeafe;  /* Светло-синий фон */
  
  /* Secondary - Стабильность */
  --secondary: #64748b;      /* Серо-синий */
  --secondary-light: #f1f5f9; /* Светло-серый */
  
  /* Accent - Действие, энергия */
  --accent: #f59e0b;         /* Оранжевый */
  --accent-hover: #d97706;
  
  /* Нейтральные */
  --background: #ffffff;
  --background-secondary: #f9fafb;
  --text-primary: #1f2937;
  --text-secondary: #6b7280;
  --border: #e5e7eb;
  
  /* Семантические */
  --success: #10b981;
  --warning: #f59e0b;
  --error: #ef4444;
  --info: #3b82f6;
}
```

**Правила использования**:
- Primary: Кнопки CTA, важные элементы
- Accent: Акценты, бейджи, иконки
- 60-30-10: 60% фон, 30% основной, 10% акцент

#### 3. Типографика

**Шрифтовая пара**: Inter + Inter

```css
/* Заголовки */
font-family: 'Inter', sans-serif;
font-weight: 600, 700;
line-height: 1.2;
letter-spacing: -0.02em;

/* Текст */
font-family: 'Inter', sans-serif;
font-weight: 400, 500;
line-height: 1.6;
letter-spacing: 0;

/* Размеры */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
```

**Иерархия**:
```
H1: text-4xl, font-bold — Главная страница
H2: text-3xl, font-bold — Разделы
H3: text-2xl, font-semibold — Подразделы
H4: text-xl, font-semibold — Группы
Body: text-base, font-normal — Основной текст
Small: text-sm, font-normal — Второстепенное
```

#### 4. Компоненты

**Кнопки**:

```tsx
// Primary CTA
<button className="px-8 py-4 bg-blue-600 text-white font-semibold rounded-lg 
                   hover:bg-blue-700 transition-all shadow-md hover:shadow-lg 
                   hover:-translate-y-0.5">
  Оставить заявку
</button>

// Secondary
<button className="px-8 py-4 bg-white text-blue-600 font-semibold rounded-lg 
                   border-2 border-blue-600 hover:bg-blue-50 transition-all">
  Узнать подробнее
</button>

// Tertiary (link)
<a href="#" className="text-blue-600 font-medium hover:underline">
  Подробнее →
</a>
```

**Карточки**:

```tsx
// Карточка услуги
<div className="p-8 border border-gray-200 rounded-xl 
                hover:border-blue-500 hover:shadow-lg transition-all 
                bg-white">
  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center 
                  justify-center mb-4">
    <HomeIcon className="w-6 h-6 text-blue-600" />
  </div>
  <h3 className="text-xl font-bold mb-2">Купить квартиру</h3>
  <p className="text-gray-600 mb-4">
    Подберём варианты по вашим критериям...
  </p>
  <a href="#" className="text-blue-600 font-medium hover:underline">
    Подробнее →
  </a>
</div>
```

**Формы**:

```tsx
// Поле ввода
<input
  type="text"
  className="w-full px-4 py-3 border border-gray-300 rounded-lg 
             focus:ring-2 focus:ring-blue-500 focus:border-blue-500 
             transition-all outline-none"
  placeholder="Ваше имя"
/>

// Кнопка отправки
<button
  type="submit"
  className="w-full px-6 py-4 bg-blue-600 text-white font-semibold 
             rounded-lg hover:bg-blue-700 transition-all shadow-md"
>
  Отправить заявку
</button>
```

#### 5. Эффекты

**Тени**:
```css
/* Лёгкие */
shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05)
shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)

/* Средние */
shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)
shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)

/* Сильные */
shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)
```

**Анимации**:
```css
/* Переходы */
transition-all: all 0.3s ease

/* Hover эффекты */
hover:-translate-y-0.5: Подъём при наведении
hover:shadow-lg: Усиление тени
hover:bg-blue-700: Изменение цвета

/* Появление */
animate-fade-in: opacity 0 → 1 за 0.5s
animate-slide-up: translateY(20px) → 0 за 0.5s
```

---

## 🛠️ Процесс работы

### Шаг 1: Сбор требований

**Вопросы пользователю**:
```
1. Какой тип продукта? (лендинг, магазин, блог, SaaS)
2. Кто целевая аудитория? (возраст, пол, интересы)
3. Какой стиль предпочитаете? (минимализм, премиум, корпоративный)
4. Есть ли брендбук? (цвета, шрифты, логотип)
5. Какие референсы нравятся? (примеры сайтов)
6. Какая платформа? (Next.js, React, Vue, HTML)
```

### Шаг 2: Генерация дизайн-системы

**Команда**:
```
/ui-ux-designer create design-system for real estate website
  --audience "buyers and sellers 25-65 years"
  --style "modern-minimal"
  --platform "nextjs-tailwind"
  --output "design-system/MASTER.md"
```

**Результат**:
```markdown
# Design System: Real Estate Website

## Brand
- Name: Ельчугин Александр - Риэлтор
- Values: Доверие, Профессионализм, Результат

## Colors
[см. раздел "Цветовая палитра" выше]

## Typography
[см. раздел "Типографика" выше]

## Components
- Buttons: Primary, Secondary, Tertiary
- Cards: Service, Property, Testimonial
- Forms: Lead Form, Contact Form, Search
- Navigation: Header, Footer, Breadcrumbs

## Effects
- Shadows: sm, md, lg, xl
- Animations: fade-in, slide-up, scale
- Borders: 8px (default), 12px (lg), 16px (xl)

## Layout
- Container: max-w-7xl mx-auto px-4
- Grid: 12 columns, 24px gap
- Spacing: 8, 16, 24, 32, 48, 64, 96, 128px
```

### Шаг 3: Создание макета

**Генерация кода**:

```tsx
// src/app/page.tsx
import { Header } from '@/components/sections/Header'
import { Hero } from '@/components/sections/Hero'
import { Services } from '@/components/sections/Services'
import { About } from '@/components/sections/About'
import { ContactForm } from '@/components/sections/ContactForm'
import { Footer } from '@/components/sections/Footer'

export default function HomePage() {
  return (
    <main className="min-h-screen bg-white">
      <Header />
      <Hero />
      <Services />
      <About />
      <ContactForm />
      <Footer />
    </main>
  )
}
```

### Шаг 4: Проверка UX

**Чеклист (99 правил)**:

**Доступность (WCAG 2.1)**:
- [ ] Контраст текста ≥ 4.5:1
- [ ] Контраст крупных элементов ≥ 3:1
- [ ] Alt text у всех изображений
- [ ] Focus виден на всех интерактивных элементах
- [ ] Навигация с клавиатуры работает

**Юзабилити**:
- [ ] Правило 3 кликов (до цели)
- [ ] Закон Фиттса (кнопки достаточного размера)
- [ ] Закон Хика (не больше 7±2 опций)
- [ ] Принцип близости (связанные элементы рядом)
- [ ] Визуальная иерархия (важное крупнее)

**Адаптивность**:
- [ ] Mobile-first подход
- [ ] Брейкпоинты: sm (640), md (768), lg (1024), xl (1280)
- [ ] Тач-целевые элементы ≥ 44px
- [ ] Шрифты читаемы на мобильных

**Производительность**:
- [ ] Изображения оптимизированы (WebP)
- [ ] Lazy loading для изображений
- [ ] Критический CSS инлайн
- [ ] Шрифты с font-display: swap

---

## 📊 Примеры генерации

### Пример 1: Лендинг риэлтора

**Запрос**:
```
Создай дизайн лендинга для риэлтора в Кирове
ЦА: семьи 30-50 лет, покупающие жильё
Стиль: доверительный, профессиональный
```

**Результат**:

**Структура**:
```
1. Header (лого, навигация, телефон)
2. Hero (фото, УТП, форма захвата)
3. Services (карточки: Купить, Продать, Арендовать)
4. About (фото, опыт, статистика)
5. Process (4 этапа работы)
6. Benefits (почему я)
7. Testimonials (отзывы клиентов)
8. Contact Form (заявка)
9. Footer (контакты, соцсети)
```

**Код Hero секции**:
```tsx
// src/components/sections/Hero.tsx
export function Hero() {
  return (
    <section className="relative py-20 bg-gradient-to-br from-blue-50 to-white">
      <div className="container mx-auto px-4">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Левая колонка: Контент */}
          <div>
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
              Ельчугин Александр
            </h1>
            <p className="text-xl text-gray-600 mb-4">
              Агент по недвижимости в Кирове
            </p>
            <p className="text-lg text-gray-600 mb-8">
              Помогу купить, продать или обменять недвижимость 
              с юридической гарантией
            </p>
            
            <div className="flex flex-wrap gap-4 mb-8">
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">500+</div>
                <div className="text-gray-500">Сделок</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">10+ лет</div>
                <div className="text-gray-500">Опыта</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">98%</div>
                <div className="text-gray-500">Довольных</div>
              </div>
            </div>
            
            <div className="flex flex-wrap gap-4">
              <a
                href="#contact"
                className="px-8 py-4 bg-blue-600 text-white font-semibold 
                         rounded-lg hover:bg-blue-700 transition-all shadow-md 
                         hover:shadow-lg hover:-translate-y-0.5"
              >
                Бесплатная консультация
              </a>
              <a
                href="tel:+7XXXXXXXXXX"
                className="px-8 py-4 bg-white text-blue-600 font-semibold 
                         rounded-lg border-2 border-blue-600 hover:bg-blue-50 
                         transition-all"
              >
                📞 +7 (XXX) XXX-XX-XX
              </a>
            </div>
          </div>
          
          {/* Правая колонка: Фото */}
          <div className="relative">
            <div className="aspect-square rounded-2xl overflow-hidden shadow-2xl">
              <Image
                src="/images/agent-photo.jpg"
                alt="Ельчугин Александр"
                fill
                className="object-cover"
              />
            </div>
            {/* Декоративный элемент */}
            <div className="absolute -bottom-6 -left-6 w-32 h-32 
                            bg-blue-100 rounded-full blur-3xl" />
          </div>
        </div>
      </div>
    </section>
  )
}
```

---

### Пример 2: Дашборд для CRM

**Запрос**:
```
Создай дизайн дашборда для CRM риэлтора
Функции: лиды, сделки, задачи, аналитика
```

**Результат**:

**Структура**:
```
1. Sidebar (навигация)
2. Top Bar (поиск, уведомления, профиль)
3. Stats Cards (4 метрики)
4. Recent Leads (таблица)
5. Deals Pipeline (канбан)
6. Tasks (список)
7. Analytics (графики)
```

**Код**:
```tsx
// src/components/Dashboard.tsx
export function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      
      <main className="ml-64 p-8">
        <TopBar />
        
        {/* Метрики */}
        <div className="grid grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Активные лиды"
            value="24"
            change="+12%"
            icon={<UsersIcon />}
          />
          <StatCard
            title="Сделки в работе"
            value="8"
            change="+2"
            icon={<BriefcaseIcon />}
          />
          <StatCard
            title="Закрыто за месяц"
            value="15"
            change="+3"
            icon={<CheckCircleIcon />}
          />
          <StatCard
            title="Выручка"
            value="450K ₽"
            change="+18%"
            icon={<CurrencyIcon />}
          />
        </div>
        
        {/* Таблица лидов */}
        <LeadsTable />
        
        {/* Канбан сделок */}
        <DealsPipeline />
      </main>
    </div>
  )
}
```

---

## 🔧 CLI команды

**Установка** (если будет CLI):
```bash
npm install -g ui-ux-designer-cli
ui-ux-designer init --ai qwen-code
```

**Генерация**:
```bash
# Создать дизайн-систему
ui-ux-designer generate design-system \
  --project "real-estate-website" \
  --style "modern-minimal" \
  --platform "nextjs-tailwind" \
  --output "design-system/"

# Создать компонент
ui-ux-designer generate component \
  --name "ServiceCard" \
  --style "modern-minimal" \
  --output "src/components/"

# Создать страницу
ui-ux-designer generate page \
  --name "LandingPage" \
  --sections "hero,services,about,contact" \
  --output "src/app/"
```

---

## 📁 Формат вывода

**Дизайн-система**:
```
design-system/
├── MASTER.md           # Основная документация
├── colors.md           # Цветовая палитра
├── typography.md       # Шрифты
├── components/
│   ├── buttons.md
│   ├── cards.md
│   ├── forms.md
│   └── navigation.md
├── effects/
│   ├── shadows.md
│   ├── animations.md
│   └── transitions.md
└── pages/
    ├── homepage.md
    ├── services.md
    └── contact.md
```

**Код**:
```
src/
├── components/
│   ├── ui/             # Базовые компоненты
│   └── sections/       # Секции страниц
├── styles/
│   └── globals.css     # Глобальные стили + Tailwind
└── app/
    ├── layout.tsx      # Layout
    └── page.tsx        # Главная
```

---

## Examples

**Триггеры для активации**:
- "создай дизайн сайта"
- "ui ux дизайн для риэлтора"
- "дизайн система"
- "design system"
- "редизайн сайта"
- "сгенерируй интерфейс"
- "create landing page design"
