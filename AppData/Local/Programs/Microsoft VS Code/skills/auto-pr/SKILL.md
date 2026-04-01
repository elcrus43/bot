---
name: auto-pr
description: |
  Автоматическая подготовка Pull Request: код-ревью, генерация документации, отправка через GitHub CLI.
  Triggers on: "pull request", "PR", "merge", "отправить код", "создать PR", "code review", "github pr"
metadata:
  version: 1.0.0
  author: elcrus43
---

# Auto PR Skill

Автоматизация создания Pull Request с полным код-ревью, документацией и отправкой через GitHub CLI.

## Tech Stack
- **VCS**: Git
- **Platform**: GitHub
- **Tools**: GitHub CLI (gh), Git
- **CI/CD**: GitHub Actions (опционально)

## Требования

### GitHub CLI
```bash
# Windows (Chocolatey)
choco install gh

# Windows (winget)
winget install GitHub.cli

# Проверка установки
gh --version
```

### Аутентификация
```bash
# Аутентификация GitHub CLI
gh auth login

# Проверка статуса
gh auth status
```

## Workflow

### Step 1: Анализ изменений
**Ввод**: Текущая ветка с изменениями
**Вывод**: Список измененных файлов, статистика

**Команды**:
```bash
# Показать статус
git status

# Показать изменения
git diff --stat

# Показать детали изменений
git diff HEAD
```

### Step 2: Код-ревью
**Ввод**: Изменения в коде
**Вывод**: Отчет о качестве кода

**Чеклист ревью**:

**Безопасность**:
- [ ] Нет захардкоженных секретов/API ключей
- [ ] Валидация пользовательского ввода
- [ ] Защита от SQL injection
- [ ] Нет уязвимостей в зависимостях

**Качество кода**:
- [ ] Следование стилю проекта (linting)
- [ ] Типизация (TypeScript/Python type hints)
- [ ] Нет дублирования кода
- [ ] Функции < 50 строк
- [ ] Понятные имена переменных/функций

**Тесты**:
- [ ] Unit тесты для новых функций
- [ ] Интеграционные тесты для API
- [ ] Тесты проходят локально
- [ ] Покрытие не уменьшилось

**Документация**:
- [ ] README обновлен (если нужно)
- [ ] Docstrings для публичных функций
- [ ] Комментарии для сложной логики
- [ ] CHANGELOG обновлен (если нужно)

### Step 3: Подготовка коммитов
**Ввод**: Изменения прошедшие ревью
**Вывод**: Закоммиченные изменения

**Conventional Commits**:
```bash
# Типы коммитов
feat:     Новая функция
fix:      Исправление бага
docs:     Документация
style:    Форматирование
refactor: Рефакторинг
test:     Тесты
chore:    Вспомогательные изменения

# Примеры
git commit -m "feat: add user authentication with JWT"
git commit -m "fix: resolve null pointer in user service"
git commit -m "docs: update API documentation"
```

**Автоматический коммит**:
```bash
# Добавить все изменения
git add .

# Коммит с описанием
git commit -m "feat: implement dashboard analytics"

# Или мульти-коммит (если несколько логических изменений)
git add src/components/Dashboard.tsx
git commit -m "feat: add dashboard component"

git add src/api/analytics.ts
git commit -m "feat: add analytics API integration"
```

### Step 4: Создание ветки
**Ввод**: Текущая ветка, название функции
**Вывод**: Новая ветка для PR

**Паттерн именования**:
```
{type}/{short-description}

Примеры:
feat/dashboard-analytics
fix/login-bug
docs/api-update
refactor/user-service
```

**Команды**:
```bash
# Создать и переключиться
git checkout -b feat/dashboard-analytics

# Или если уже на ветке
git branch -M feat/dashboard-analytics
```

### Step 5: Push и создание PR
**Ввод**: Локальная ветка с изменениями
**Вывод**: Pull Request на GitHub

**Команды**:
```bash
# Push ветки
git push -u origin feat/dashboard-analytics

# Создание PR
gh pr create \
  --title "feat: Add dashboard analytics" \
  --body "## Changes
- Added dashboard component with charts
- Integrated analytics API
- Added unit tests

## Testing
- [x] Unit tests pass
- [x] Manual testing completed

## Screenshots
[Add if UI changes]" \
  --base main \
  --label "feature" \
  --assignee "@me" \
  --reviewer "team-lead"
```

### Step 6: Генерация описания PR
**Ввод**: Список изменений, коммиты
**Вывод**: Структурированное описание PR

**Шаблон PR**:
```markdown
## Description
[Краткое описание изменений]

## Type of Change
- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to change)
- [ ] 📚 Documentation update
- [ ] 🧹 Refactoring
- [ ] ⚡ Performance improvement
- [ ] 🧪 Test update

## Changes
- [Список основных изменений]

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Screenshots (if applicable)
[Изображения или GIF для UI изменений]

## Checklist
- [ ] Code follows project guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests pass locally
```

## Constraints

**MUST**:
- Использовать Conventional Commits
- Запускать тесты перед коммитом
- Проверять код через linter
- Создавать информативное описание PR
- Добавлять reviewers из команды
- Связывать с issues (если есть)

**MUST NOT**:
- Не пушить в main/master напрямую
- Не создавать PR без тестов
- Не игнорировать warnings
- Не коммитить .env и секреты
- Не создавать огромные PR (>400 строк)

## Examples

### Пример 1: Новая функция
**Запрос**: "Создай PR для новой функции авторизации"

**Workflow**:
1. Проверить изменения: `git diff --stat`
2. Запустить тесты: `npm test` или `pytest`
3. Запустить линтер: `npm run lint` или `ruff check`
4. Создать коммит: `git commit -m "feat: add JWT authentication"`
5. Создать ветку: `git checkout -b feat/jwt-auth`
6. Push: `git push -u origin feat/jwt-auth`
7. Создать PR:
```bash
gh pr create \
  --title "feat: Add JWT authentication" \
  --body "## Changes
- Implemented JWT token generation and validation
- Added login/logout endpoints
- Added unit tests for auth service

## Testing
- [x] Unit tests pass (15 new tests)
- [x] Manual testing with Postman

## Security
- [x] No secrets in code
- [x] Input validation added" \
  --base main
```

### Пример 2: Исправление бага
**Запрос**: "Отправь фикс для бага с авторизацией"

**Workflow**:
1. Проверить изменения
2. Запустить тесты
3. Коммит: `git commit -m "fix: resolve token expiration issue"`
4. Ветка: `git checkout -b fix/token-expiration`
5. Push и PR:
```bash
gh pr create \
  --title "fix: Resolve token expiration issue" \
  --body "Fixes #123

## Changes
- Fixed token expiration check
- Added refresh token logic

## Testing
- [x] Reproduced bug before fix
- [x] Verified fix resolves issue" \
  --base main
```

## Communication
- Спрашивать подтверждение перед push
- Показывать summary изменений
- Предлагать улучшить описание PR
- Напоминать о reviewers
