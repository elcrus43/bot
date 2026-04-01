---
name: seo-analyzer
description: |
  Полный SEO аудит сайта: технический, контент, E-E-A-T, Core Web Vitals, schema.org.
  Triggers on: "seo аудит", "проверить seo", "оптимизация сайта", "seo analysis", "seo yelchugin.ru"
metadata:
  version: 1.0.0
  author: elcrus43 (adapted from Agentic-SEO-Skill)
---

# SEO Analyzer Skill

Профессиональный SEO аудит сайтов с использованием агентского подхода. Адаптировано из [Agentic-SEO-Skill](https://github.com/Bhanunamikaze/Agentic-SEO-Skill).

## 🎯 Что анализирует

### 1. Технический SEO (Technical SEO)

**Проверка**:
- [ ] **Robots.txt** — доступность, правила блокировки
- [ ] **Sitemap.xml** — наличие, актуальность, ошибки
- [ ] **SSL сертификат** — HTTPS, смешанный контент
- [ ] **Canonical URLs** — дубли страниц, правильные canonical
- [ ] **Redirects** — 301, 302, redirect chains, loops
- [ ] **404 ошибки** — битые ссылки, missing pages
- [ ] **Crawlability** — доступность для поисковиков

**Инструменты**:
```python
# Проверка robots.txt
import requests
response = requests.get("https://yelchugin.ru/robots.txt")
print(response.text)

# Проверка sitemap
sitemap = requests.get("https://yelchugin.ru/sitemap.xml")
# Анализ URL в sitemap

# Проверка HTTPS
import ssl
import socket
context = ssl.create_default_context()
with socket.create_connection((domain, 443)) as sock:
    with context.wrap_socket(sock, server_hostname=domain) as ssock:
        print(ssock.version())
```

---

### 2. On-Page SEO

**Анализ каждой страницы**:

**Meta tags**:
```html
<!-- Проверка -->
<title>Длина: 50-60 символов, ключевые слова в начале</title>
<meta name="description" content="Длина: 150-160 символов, УТП, CTA">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://yelchugin.ru/">
```

**Заголовки**:
```
H1: 1 на странице, ключевые слова
H2: 3-6, структура контента
H3-H6: иерархия, логика
```

**Контент**:
- Уникальность текста
- Плотность ключевых слов (1-3%)
- LSI слова (тематические)
- Длина контента (1000+ слов для услуг)
- Мультимедиа (фото, видео, инфографика)

**Внутренние ссылки**:
- Перелинковка между страницами
- Anchor text (разнообразный)
- Глубина кликов (до 3 уровней)

---

### 3. E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)

**Проверка для сайта риэлтора**:

**Experience (Опыт)**:
- [ ] Кейсы с реальными объектами
- [ ] Фото "до/после"
- [ ] Истории клиентов
- [ ] Количество сделок (500+)

**Expertise (Экспертность)**:
- [ ] Образование, сертификаты
- [ ] Опыт работы (10+ лет)
- [ ] Специализация (риэлтор, юрист)
- [ ] Публикации, СМИ

**Authoritativeness (Авторитетность)**:
- [ ] Отзывы на независимых платформах
- [ ] Награды, рейтинги
- [ ] Партнёрства (банки, застройщики)
- [ ] Членство в ассоциациях

**Trustworthiness (Надёжность)**:
- [ ] Контакты (адрес, телефон, email)
- [ ] Политика конфиденциальности
- [ ] Договор оферты
- [ ] SSL сертификат
- [ ] Реальные фото (не стоковые)

---

### 4. Core Web Vitals

**Метрики Google**:

**LCP (Largest Contentful Paint)**:
- **Норма**: < 2.5 сек
- **Проверка**: PageSpeed Insights API
- **Улучшение**: оптимизация изображений, кэширование

**FID (First Input Delay)**:
- **Норма**: < 100 мс
- **Проверка**: Chrome User Experience Report
- **Улучшение**: минимизация JS, code splitting

**CLS (Cumulative Layout Shift)**:
- **Норма**: < 0.1
- **Проверка**: Lighthouse
- **Улучшение**: фиксированные размеры, font-display: swap

**Проверка через API**:
```python
import requests

def check_pagespeed(url, api_key):
    response = requests.get(
        f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed",
        params={
            "url": url,
            "key": api_key,
            "category": "PERFORMANCE",
            "strategy": "mobile"
        }
    )
    data = response.json()
    
    lcp = data['lighthouseResult']['audits']['largest-contentful-paint']['numericValue']
    fid = data['lighthouseResult']['audits']['max-potential-fid']['numericValue']
    cls = data['lighthouseResult']['audits']['cumulative-layout-shift']['numericValue']
    
    return {
        "lcp": lcp / 1000,  # секунды
        "fid": fid / 1000,  # секунды
        "cls": cls,
        "passed": lcp < 2500 and fid < 100 and cls < 0.1
    }
```

---

### 5. Schema.org Markup

**Проверка микроразметки**:

**Для риэлтора**:
```json
{
  "@context": "https://schema.org",
  "@type": "RealEstateAgent",
  "name": "Ельчугин Александр",
  "description": "Агент по недвижимости в Кирове",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Киров",
    "streetAddress": "..."
  },
  "telephone": "+7 (XXX) XXX-XX-XX",
  "email": "...",
  "url": "https://yelchugin.ru",
  "logo": "https://yelchugin.ru/logo.png",
  "openingHours": "Mo-Fr 09:00-18:00",
  "priceRange": "₽₽",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "150"
  }
}
```

**Проверка**:
```python
import requests
from bs4 import BeautifulSoup

def check_schema(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # JSON-LD
    json_ld = soup.find('script', type='application/ld+json')
    if json_ld:
        print("✅ JSON-LD найден")
        # Валидация через Google Rich Results Test API
    
    # Microdata
    microdata = soup.find_all(attrs={"itemscope": True})
    if microdata:
        print(f"✅ Microdata: {len(microdata)} элементов")
    
    # RDFa
    rdfa = soup.find_all(attrs={"vocab": True})
    if rdfa:
        print(f"✅ RDFa: {len(rdfa)} элементов")
```

---

### 6. Контент-анализ

**Анализ текстов**:

**Параметры**:
- Длина текста (слов)
- Уникальность (%)
- Тошнота (ключевые слова)
- Водность (стоп-слова)
- Читаемость (Индекс Флеша)

**Проверка**:
```python
def analyze_content(text):
    words = len(text.split())
    sentences = text.count('.') + text.count('!') + text.count('?')
    syllables = sum(sum(1 for char in word if char in 'аеёиоуыэюя') for word in text.split())
    
    # Индекс Флеша (читаемость)
    flesch = 206.835 - 1.3 * (words / sentences) - 60.1 * (syllables / words)
    
    return {
        "words": words,
        "sentences": sentences,
        "flesch_score": flesch,
        "readability": "easy" if flesch > 70 else "medium" if flesch > 40 else "hard"
    }
```

**E-E-A-T сигналы в контенте**:
- Упоминание опыта ("10 лет на рынке")
- Конкретные цифры ("500+ сделок")
- Реальные кейсы (адреса, цены, фото)
- Отзывы клиентов (имена, фото)
- Сертификаты, награды

---

## 🛠️ Процесс аудита

### Шаг 1: Сканирование сайта

**Сбор информации**:
```bash
# 1. Карта сайта
curl -s https://yelchugin.ru/sitemap.xml | grep -o '<loc>[^<]*</loc>'

# 2. Проверка robots.txt
curl -s https://yelchugin.ru/robots.txt

# 3. Заголовки
curl -I https://yelchugin.ru

# 4. HTML для анализа
curl -s https://yelchugin.ru > yelchugin.html
```

### Шаг 2: Запуск скриптов анализа

**Автоматическая проверка**:
```python
# scripts/seo_audit.py
import requests
from bs4 import BeautifulSoup
import json

class SEOAuditor:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
    
    def audit(self):
        report = {
            "url": self.url,
            "technical": self.technical_audit(),
            "onpage": self.onpage_audit(),
            "content": self.content_audit(),
            "performance": self.performance_audit(),
            "schema": self.schema_audit()
        }
        return report
    
    def technical_audit(self):
        # Проверка HTTPS, redirects, robots.txt, sitemap
        pass
    
    def onpage_audit(self):
        # Meta tags, заголовки, ссылки
        pass
    
    def content_audit(self):
        # Уникальность, ключевые слова, E-E-A-T
        pass
    
    def performance_audit(self):
        # Core Web Vitals через PageSpeed API
        pass
    
    def schema_audit(self):
        # Schema.org markup
        pass

# Запуск
auditor = SEOAuditor("https://yelchugin.ru")
report = auditor.audit()
print(json.dumps(report, indent=2))
```

### Шаг 3: Генерация отчёта

**Формат отчёта**:

```markdown
# SEO Audit Report: yelchugin.ru

## Summary
- **Overall Score**: 78/100
- **Technical**: 85/100 ✅
- **On-Page**: 72/100 ⚠️
- **Content**: 80/100 ✅
- **Performance**: 65/100 ⚠️
- **Schema**: 90/100 ✅

## Critical Issues (3)

### 1. Missing H1 on Homepage
- **Page**: /
- **Impact**: High
- **Fix**: Add <h1>Ельчугин Александр - Агент по недвижимости в Кирове</h1>

### 2. Slow LCP (3.8s)
- **Page**: /
- **Impact**: High (Core Web Vitals)
- **Fix**: Optimize hero image, enable lazy loading

### 3. No FAQ Schema
- **Page**: /services
- **Impact**: Medium (Rich Results)
- **Fix**: Add FAQPage schema markup

## Recommendations (12)

### High Priority
1. Add H1 to all pages
2. Optimize images (WebP format)
3. Implement FAQ schema

### Medium Priority
4. Increase content length on service pages
5. Add internal linking between services
6. Create blog section

### Low Priority
7. Add Open Graph tags for social sharing
8. Implement breadcrumbs
9. Add video testimonials
```

### Шаг 4: План действий

**Action Plan**:

```markdown
# SEO Action Plan: yelchugin.ru

## Week 1-2: Technical Fixes
- [ ] Fix missing H1 tags
- [ ] Optimize images (compress, WebP)
- [ ] Enable caching
- [ ] Fix 404 errors

## Week 3-4: On-Page Optimization
- [ ] Rewrite meta descriptions
- [ ] Add internal links
- [ ] Implement schema markup
- [ ] Fix heading hierarchy

## Month 2: Content Strategy
- [ ] Write 5 blog posts (ипотека, район, советы)
- [ ] Add 10 case studies
- [ ] Collect 20 video testimonials
- [ ] Create neighborhood guides

## Month 3: Link Building
- [ ] Submit to local directories
- [ ] Partner with local businesses
- [ ] Guest posts on real estate blogs
- [ ] Social media presence
```

---

## 📊 SEO чеклист для yelchugin.ru

### Технический SEO
- [ ] HTTPS везде (no mixed content)
- [ ] Robots.txt разрешает индексацию
- [ ] Sitemap.xml актуален
- [ ] Canonical URLs на всех страницах
- [ ] Нет битых ссылок (404)
- [ ] 301 редиректы со старых URL

### On-Page SEO
- [ ] Уникальные Title (50-60 символов)
- [ ] Уникальные Description (150-160 символов)
- [ ] H1 на каждой странице (1 шт)
- [ ] H2-H6 иерархия
- [ ] Alt text у всех изображений
- [ ] Внутренняя перелинковка

### Контент
- [ ] 1000+ слов на страницах услуг
- [ ] Кейсы с фото и цифрами
- [ ] Отзывы с именами и фото
- [ ] Блог (2+ статьи в месяц)
- [ ] FAQ по каждой услуге
- [ ] Гайды по районам Кирова

### E-E-A-T
- [ ] Страница "Обо мне" с фото и историей
- [ ] Сертификаты и награды
- [ ] Партнёры (банки, застройщики)
- [ ] Реальный адрес и телефон
- [ ] Политика конфиденциальности

### Schema.org
- [ ] RealEstateAgent schema
- [ ] Service schema для услуг
- [ ] FAQPage schema
- [ ] Review schema
- [ ] BreadcrumbList schema

### Core Web Vitals
- [ ] LCP < 2.5 сек
- [ ] FID < 100 мс
- [ ] CLS < 0.1
- [ ] Mobile-friendly
- [ ] No intrusive interstitials

---

## 🔧 Инструменты

### Онлайн-сервисы:
- [Google PageSpeed Insights](https://pagespeed.web.dev/)
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Screaming Frog](https://www.screamingfrog.co.uk/seo-spider/) (1-500 URL бесплатно)
- [Ahrefs Webmaster Tools](https://ahrefs.com/webmaster-tools) (бесплатно)
- [Google Search Console](https://search.google.com/search-console)

### Python скрипты:
```bash
# Установить зависимости
pip install requests beautifulsoup4 lxml

# Запустить аудит
python scripts/seo_audit.py https://yelchugin.ru

# Проверить PageSpeed
python scripts/pagespeed_check.py https://yelchugin.ru

# Проверить Schema
python scripts/schema_validator.py https://yelchugin.ru
```

---

## 📈 Метрики успеха

**Через 1 месяц**:
- ✅ Все технические ошибки исправлены
- ✅ Meta tags оптимизированы
- ✅ Schema.org добавлена

**Через 3 месяца**:
- ✅ Позиции в ТОП-10 по 5+ запросам
- ✅ Органический трафик +30%
- ✅ Core Web Vitals в зелёной зоне

**Через 6 месяцев**:
- ✅ ТОП-3 по локальным запросам
- ✅ Органический трафик +100%
- ✅ 20+ лидов в месяц из поиска

---

## Examples

**Триггеры для активации**:
- "сделай seo аудит yelchugin.ru"
- "проверить seo оптимизацию сайта"
- "seo analysis"
- "оптимизировать сайт для поисковиков"
- "technical seo check"
- "core web vitals audit"
