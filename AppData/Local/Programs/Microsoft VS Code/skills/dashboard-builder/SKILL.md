---
name: dashboard-builder
description: |
  Создание full-stack дашбордов с React/Next.js + shadcn/ui + Tailwind CSS + Recharts.
  Triggers on: "dashboard", "дашборд", "charts", "графики", "analytics", "статистика", "visualization"
metadata:
  version: 1.0.0
  author: elcrus43
---

# Dashboard Builder Skill

Автоматическое создание профессиональных дашбордов с графиками, таблицами и метриками.

## Tech Stack
- **Frontend**: Next.js 15 (App Router), React 19, TypeScript 5 (strict mode)
- **UI Components**: shadcn/ui
- **Styling**: Tailwind CSS v4
- **Charts**: Recharts или Chart.js
- **State**: Zustand или React Context
- **Data Fetching**: TanStack Query (React Query)

## Workflow

### Step 1: Анализ требований
**Ввод**: Описание пользователя (какие данные, метрики, графики нужны)
**Вывод**: Список компонентов и структура дашборда
**Условие завершения**: Утвержденная структура с пользователем

**Действия**:
1. Уточнить тип дашборда (analytics, admin, monitoring, etc.)
2. Определить источники данных (API, mock data, database)
3. Выбрать типы графиков (line, bar, pie, area, radar)
4. Определить ключевые метрики (KPI cards)

### Step 2: Создание структуры проекта
**Ввод**: Утвержденная структура
**Вывод**: Созданные файлы и директории
**Условие завершения**: Все файлы созданы, зависимости установлены

**Команды**:
```bash
# Создание Next.js проекта с TypeScript
npx create-next-app@latest dashboard --typescript --tailwind --app --eslint

# Установка зависимостей
cd dashboard
npm install recharts lucide-react class-variance-authority clsx tailwind-merge

# Установка shadcn/ui
npx shadcn-ui@latest init
npx shadcn-ui@latest add card button table select tabs
```

### Step 3: Создание компонентов
**Ввод**: Структура компонентов
**Вывод**: Готовые React компоненты

**Структура компонентов**:
```
src/
├── components/
│   ├── ui/           # shadcn/ui компоненты
│   ├── charts/       # компоненты графиков
│   ├── dashboard/    # компоненты дашборда
│   └── layout/       # layout компоненты
├── app/
│   ├── page.tsx      # главная страница
│   ├── layout.tsx    # основной layout
│   └── api/          # API routes
└── lib/
    ├── utils.ts      # утилиты
    └── types.ts      # TypeScript типы
```

### Step 4: Реализация графиков
**Примеры компонентов**:

**LineChart Component**:
```typescript
'use client'

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface ChartData {
  name: string
  value: number
}

interface Props {
  data: ChartData[]
  title: string
}

export function DashboardLineChart({ data, title }: Props) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
```

**KPI Card Component**:
```typescript
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface KPICardProps {
  title: string
  value: string | number
  change?: number
  icon?: React.ReactNode
}

export function KPICard({ title, value, change, icon }: KPICardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {icon}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {change && (
          <p className={`text-xs ${change >= 0 ? 'text-green-500' : 'text-red-500'}`}>
            {change >= 0 ? '+' : ''}{change}% from last month
          </p>
        )}
      </CardContent>
    </Card>
  )
}
```

### Step 5: Тестирование и сборка
**Команды**:
```bash
# Запуск dev сервера
npm run dev

# Тип чек
npm run type-check

# Линт
npm run lint

# Сборка
npm run build
```

## Constraints

**MUST**:
- Использовать TypeScript strict mode
- Все компоненты должны быть typed
- Использовать Tailwind CSS для стилизации
- Адаптивный дизайн (mobile-first)
- Dark mode поддержка
- Loading states для всех графиков
- Error boundaries

**MUST NOT**:
- Не использовать any типы
- Не хардкодить данные (использовать mock или API)
- Не игнорировать error handling
- Не создавать компоненты больше 200 строк

## Communication
- Быть кратким, объяснять "почему", а не только "что"
- Показывать превью после создания каждого компонента
- Спрашивать подтверждение перед изменением структуры
- Предлагать простейшее рабочее решение сначала

## Examples

**Пример запроса**: "Создай дашборд для аналитики продаж с графиками по месяцам"

**Ответ**:
1. Создать Next.js проект с shadcn/ui
2. Добавить компоненты: KPICard, LineChart, BarChart, DataTable
3. Создать mock данные для продаж
4. Реализовать главную страницу с метриками:
   - Total Revenue
   - Orders Count
   - Average Order Value
   - Growth Rate
