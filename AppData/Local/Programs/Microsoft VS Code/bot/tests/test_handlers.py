# Тесты для handlers.py
# Запуск: pytest tests/test_handlers.py -v

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from aiogram.types import Message, CallbackQuery, User
from aiogram.fsm.context import FSMContext


@pytest.fixture
def mock_user():
    """Фикстура тестового пользователя."""
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
    return Message(
        message_id=1,
        date=1234567890,
        chat={"id": 123456789, "type": "private", "first_name": "Test"},
        from_user=mock_user,
        text="/start"
    )


@pytest.fixture
def mock_callback(mock_user):
    """Фикстура тестового callback query."""
    callback = MagicMock(spec=CallbackQuery)
    callback.from_user = mock_user
    callback.message = MagicMock()
    callback.answer = AsyncMock()
    return callback


@pytest.mark.asyncio
async def test_cmd_start(mock_message):
    """Тест команды /start."""
    from handlers_new import router
    
    # Моки для зависимостей
    with patch('handlers_new.save_lead', return_value={"id": "test-lead-id"}):
        with patch.object(mock_message, 'answer', new_callable=AsyncMock) as mock_answer:
            # Имитация вызова хендлера
            await router.propagate_event(
                "message",
                mock_message,
                _handler=None
            )
            
            # Проверка что ответ был отправлен
            mock_answer.assert_called_once()
            call_args = mock_answer.call_args[0][0]
            assert "Здравствуйте" in call_args
            assert "🏠 Купить квартиру" in call_args


@pytest.mark.asyncio
async def test_cmd_help(mock_message):
    """Тест команды /help."""
    from handlers_new import router
    
    mock_message.text = "/help"
    
    with patch.object(mock_message, 'answer', new_callable=AsyncMock) as mock_answer:
        await router.propagate_event(
            "message",
            mock_message,
            _handler=None
        )
        
        mock_answer.assert_called_once()
        call_args = mock_answer.call_args[0][0]
        assert "🏡 Что я умею" in call_args


@pytest.mark.asyncio
async def test_cmd_stats_admin(mock_message):
    """Тест команды /stats для админа."""
    from handlers_new import router, ADMIN_IDS
    
    # Добавляем пользователя в админы
    with patch('handlers_new.ADMIN_IDS', [mock_message.from_user.id]):
        with patch('handlers_new.get_stats', return_value={
            "leads_24h": 5,
            "messages_24h": 42,
            "interest_buy": 10
        }):
            with patch('handlers_new.count_leads', return_value=100):
                with patch.object(mock_message, 'answer', new_callable=AsyncMock) as mock_answer:
                    mock_message.text = "/stats"
                    
                    await router.propagate_event(
                        "message",
                        mock_message,
                        _handler=None
                    )
                    
                    mock_answer.assert_called_once()
                    call_args = mock_answer.call_args[0][0]
                    assert "📊" in call_args
                    assert "Всего лидов: 100" in call_args


@pytest.mark.asyncio
async def test_cmd_stats_not_admin(mock_message):
    """Тест команды /stats для не админа."""
    from handlers_new import router
    
    # Пользователь не в списке админов
    with patch('handlers_new.ADMIN_IDS', [999999]):
        with patch.object(mock_message, 'answer', new_callable=AsyncMock) as mock_answer:
            mock_message.text = "/stats"
            
            await router.propagate_event(
                "message",
                mock_message,
                _handler=None
            )
            
            mock_answer.assert_called_once()
            call_args = mock_answer.call_args[0][0]
            assert "❌ У вас нет прав" in call_args


@pytest.mark.asyncio
async def test_process_phone_valid(mock_message):
    """Тест валидации телефона - корректный номер."""
    from handlers_new import router, LeadForm
    from handlers_new import is_valid_phone
    
    # Проверка валидации
    assert is_valid_phone("+7 (999) 123-45-67") is True
    assert is_valid_phone("89991234567") is True
    assert is_valid_phone("+79991234567") is True


@pytest.mark.asyncio
async def test_process_phone_invalid(mock_message):
    """Тест валидации телефона - некорректный номер."""
    from handlers_new import is_valid_phone
    
    assert is_valid_phone("abc") is False
    assert is_valid_phone("123") is False
    assert is_valid_phone("@hacker") is False
    assert is_valid_phone("") is False


@pytest.mark.asyncio
async def test_process_name_valid(mock_message):
    """Тест валидации имени - корректное имя."""
    from handlers_new import is_valid_name
    
    assert is_valid_name("Иван") is True
    assert is_valid_name("John") is True
    assert is_valid_name("Анна-Мария") is True
    assert is_valid_name("Сергей Иванович") is True


@pytest.mark.asyncio
async def test_process_name_invalid(mock_message):
    """Тест валидации имени - некорректное имя."""
    from handlers_new import is_valid_name
    
    assert is_valid_name("A") is False  # Слишком короткое
    assert is_valid_name("123") is False  # Цифры
    assert is_valid_name("@username") is False  # Спецсимволы
    assert is_valid_name("") is False


@pytest.mark.asyncio
async def test_handle_interest_buy(mock_callback):
    """Тест выбора интереса - покупка."""
    from handlers_new import router
    
    mock_callback.data = "interest_buy"
    
    with patch('handlers_new.save_lead', return_value={"id": "lead-id", "interest": "купить"}):
        with patch('handlers_new.save_message', return_value={"id": "msg-id"}):
            with patch.object(mock_callback.message, 'edit_text', new_callable=AsyncMock) as mock_edit:
                with patch.object(mock_callback, 'answer', new_callable=AsyncMock):
                    await router.propagate_event(
                        "callback_query",
                        mock_callback,
                        _handler=None
                    )
                    
                    mock_edit.assert_called_once()
                    call_args = mock_edit.call_args[0][0]
                    assert "купить недвижимость" in call_args


@pytest.mark.asyncio
async def test_handle_message(mock_message):
    """Тест обработки обычного сообщения."""
    from handlers_new import router
    
    mock_message.text = "Какой район лучше для семьи?"
    
    with patch('handlers_new.get_lead_by_telegram_id', return_value={"id": "lead-id"}):
        with patch('handlers_new.save_message', return_value={"id": "msg-id"}):
            with patch('handlers_new.get_messages_for_lead', return_value=[]):
                with patch('handlers_new.get_ai_response', return_value="Отличный вопрос!"):
                    with patch.object(mock_message, 'answer', new_callable=AsyncMock) as mock_answer:
                        with patch.object(mock_message.bot, 'send_chat_action', new_callable=AsyncMock):
                            await router.propagate_event(
                                "message",
                                mock_message,
                                _handler=None
                            )
                            
                            mock_answer.assert_called()
                            call_args = mock_answer.call_args[0][0]
                            assert "Отличный вопрос!" in call_args


@pytest.mark.asyncio
async def test_handle_message_error(mock_message):
    """Тест обработки ошибки в handle_message."""
    from handlers_new import router
    
    mock_message.text = "Тестовое сообщение"
    
    with patch('handlers_new.get_lead_by_telegram_id', side_effect=Exception("DB error")):
        with patch.object(mock_message, 'answer', new_callable=AsyncMock) as mock_answer:
            await router.propagate_event(
                "message",
                mock_message,
                _handler=None
            )
            
            # Должна быть показана ошибка
            mock_answer.assert_called()
            call_args = mock_answer.call_args[0][0]
            assert "ошибка" in call_args.lower()
