---
name: image-generation
description: |
  Генерация изображений по тексту через DashScope API (Wanx модель).
  Triggers on: "изображение", "image", "картинка", "generate image", "сгенерировать", "logo", "icon", "banner"
metadata:
  version: 1.0.0
  author: elcrus43
---

# Image Generation Skill

Генерация изображений по текстовому описанию с использованием DashScope API (Alibaba Cloud Wanx модель).

## Tech Stack
- **API**: DashScope API (Alibaba Cloud)
- **Model**: Wanx (wanx-v1)
- **Language**: Python или Node.js
- **Output**: PNG, JPG, WebP

## Требования

### API Key
Необходим API ключ DashScope:
- Получить: https://dashscope.console.aliyun.com/
- Установить переменную окружения: `DASHSCOPE_API_KEY`

### Зависимости

**Python**:
```bash
pip install dashscope
```

**Node.js**:
```bash
npm install dashscope
```

## Workflow

### Step 1: Подготовка промпта
**Ввод**: Описание изображения от пользователя
**Вывод**: Оптимизированный промпт для генерации

**Правила оптимизации промпта**:
- Быть конкретным и детальным
- Указывать стиль (realistic, illustration, minimal, etc.)
- Указывать цветовую палитру
- Указывать разрешение (если важно)
- Избегать противоречивых описаний

### Step 2: Генерация изображения
**Ввод**: Оптимизированный промпт
**Вывод**: URL сгенерированного изображения

**Python пример**:
```python
import dashscope
from dashscope import ImageSynthesis

dashscope.api_key = "YOUR_API_KEY"

def generate_image(prompt, size='1024*1024'):
    rsp = ImageSynthesis.call(
        model=ImageSynthesis.Models.wanx_v1,
        prompt=prompt,
        n=1,
        size=size
    )
    
    if rsp.status_code == 200:
        return rsp.output.results[0].url
    else:
        raise Exception(f"Error: {rsp.code} - {rsp.message}")

# Пример использования
url = generate_image("modern minimalist logo for tech company, blue and white colors")
print(f"Generated image: {url}")
```

**Node.js пример**:
```typescript
import DashScope from 'dashscope'

const client = new DashScope({
  apiKey: process.env.DASHSCOPE_API_KEY
})

async function generateImage(prompt: string, size: string = '1024*1024') {
  const response = await client.imageSynthesis.call({
    model: 'wanx-v1',
    prompt: prompt,
    n: 1,
    size: size
  })
  
  if (response.status === 200) {
    return response.output.results[0].url
  } else {
    throw new Error(`Error: ${response.code} - ${response.message}`)
  }
}

// Пример использования
const url = await generateImage("modern minimalist logo for tech company, blue and white colors")
console.log(`Generated image: ${url}`)
```

### Step 3: Сохранение изображения
**Ввод**: URL изображения
**Вывод**: Локальный файл

**Python**:
```python
import requests

def download_image(url: str, output_path: str):
    response = requests.get(url)
    response.raise_for_status()
    
    with open(output_path, 'wb') as f:
        f.write(response.content)
    
    return output_path
```

**Node.js**:
```typescript
import fs from 'fs'
import https from 'https'

function downloadImage(url: string, outputPath: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(outputPath)
    
    https.get(url, (response) => {
      response.pipe(file)
      file.on('finish', () => {
        file.close()
        resolve(outputPath)
      })
    }).on('error', (err) => {
      fs.unlink(outputPath, () => reject(err))
      reject(err)
    })
  })
}
```

## Constraints

**MUST**:
- Проверять наличие API ключа перед генерацией
- Обрабатывать ошибки API gracefully
- Сохранять изображения в формате PNG или JPG
- Показывать превью после генерации
- Кэшировать сгенерированные изображения

**MUST NOT**:
- Не генерировать контент для взрослых
- Не нарушать авторские права
- Не использовать для deepfakes
- Не хранить API ключи в коде

## Examples

### Пример 1: Логотип
**Запрос**: "Создай логотип для кофейни"

**Оптимизированный промпт**:
```
minimalist coffee shop logo, coffee cup icon, warm brown and cream colors, 
vector style, clean lines, modern design, white background
```

### Пример 2: Баннер
**Запрос**: "Нужен баннер для сайта"

**Оптимизированный промпт**:
```
website hero banner, technology theme, abstract digital network background, 
blue gradient, modern corporate style, 1920x1080, professional look
```

### Пример 3: Иконка
**Запрос**: "Иконка для приложения"

**Оптимизированный промпт**:
```
mobile app icon, rounded square, gradient purple to pink, 
simple geometric shape, iOS style, 1024x1024, app store ready
```

## Communication
- Спрашивать детали перед генерацией (стиль, цвета, назначение)
- Показывать несколько вариантов если возможно
- Предлагать альтернативные промпты для лучших результатов
- Объяснять ограничения модели
