"""
Кастомный Rate Limit middleware для aiogram 3.x
"""
import asyncio
import logging
from functools import wraps
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from cachetools import TTLCache

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseMiddleware):
    """
    Middleware для ограничения частоты сообщений.
    """
    
    def __init__(self, limit: float = 3.0):
        """
        Args:
            limit: Минимальное время между сообщениями в секундах
        """
        self.limit = limit
        self.caches = {}
        super().__init__()
    
    async def __call__(self, handler, event, data):
        # Получаем ID пользователя
        user_id = None
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        
        if user_id is None:
            return await handler(event, data)
        
        # Создаём кэш для этого типа событий если нет
        if type(event) not in self.caches:
            self.caches[type(event)] = TTLCache(maxsize=10000, ttl=self.limit * 2)
        
        cache = self.caches[type(event)]
        
        # Проверяем лимит
        if user_id in cache:
            logger.warning(f"Rate limit exceeded for user {user_id}")
            if isinstance(event, Message):
                await event.answer("⏳ Пожалуйста, не спамьте. Подождите немного.")
            return None
        
        # Запоминаем время последнего сообщения
        cache[user_id] = True
        
        return await handler(event, data)


def rate_limit(limit: float = 3.0):
    """
    Декоратор для ограничения частоты вызовов функций.
    
    Usage:
        @rate_limit(limit=3.0)
        async def my_handler(message: Message):
            ...
    """
    def decorator(func):
        caches = {}
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Пытаемся получить user_id из аргументов
            message = None
            for arg in args:
                if isinstance(arg, Message):
                    message = arg
                    break
            
            if message is None:
                return await func(*args, **kwargs)
            
            user_id = message.from_user.id
            
            if user_id not in caches:
                caches[user_id] = TTLCache(maxsize=1, ttl=limit)
            
            if user_id in caches[user_id]:
                logger.debug(f"Rate limit hit for user {user_id}")
                return None
            
            caches[user_id][user_id] = True
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator
