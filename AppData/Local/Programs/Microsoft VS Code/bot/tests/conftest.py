# Конфигурация pytest и фикстуры
# Запуск: pytest -v

import pytest
import os
from unittest.mock import AsyncMock, patch


# Настройка тестового окружения
@pytest.fixture(autouse=True)
def setup_env():
    """Автоматическая настройка переменных окружения для тестов."""
    os.environ["BOT_TOKEN"] = "test_bot_token"
    os.environ["GROQ_API_KEY"] = "test_groq_key"
    os.environ["SUPABASE_URL"] = "https://test.supabase.co"
    os.environ["SUPABASE_KEY"] = "test_key"
    os.environ["REALTOR_TELEGRAM_ID"] = "123456789"
    os.environ["ADMIN_IDS"] = "123456789"
    os.environ["MAX_HISTORY_MESSAGES"] = "20"
    yield
    # Очистка после теста
    for key in ["BOT_TOKEN", "GROQ_API_KEY", "SUPABASE_URL", "SUPABASE_KEY", 
                "REALTOR_TELEGRAM_ID", "ADMIN_IDS", "MAX_HISTORY_MESSAGES"]:
        if key in os.environ:
            del os.environ[key]


@pytest.fixture
def mock_user():
    """Фикстура тестового пользователя Telegram."""
    from aiogram.types import User
    return User(
        id=123456789,
        is_bot=False,
        first_name="Test",
        last_name="User",
        username="testuser"
    )


@pytest.fixture
def mock_message(mock_user):
    """Фикстура тестового сообщения."""
    from aiogram.types import Message
    return Message(
        message_id=1,
        date=1234567890,
        chat={"id": 123456789, "type": "private", "first_name": "Test"},
        from_user=mock_user
    )


@pytest.fixture
def mock_callback(mock_user):
    """Фикстура тестового callback query."""
    from unittest.mock import MagicMock
    from aiogram.types import CallbackQuery
    
    callback = MagicMock(spec=CallbackQuery)
    callback.from_user = mock_user
    callback.message = MagicMock()
    callback.answer = AsyncMock()
    callback.message.edit_text = AsyncMock()
    return callback


@pytest.fixture
def mock_state():
    """Фикстура FSM состояния."""
    state = AsyncMock(spec=FSMContext)
    state.get_data = AsyncMock(return_value={})
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()
    state.clear = AsyncMock()
    return state


# Импорты для тестов
from unittest.mock import patch, AsyncMock, MagicMock
import pytest
