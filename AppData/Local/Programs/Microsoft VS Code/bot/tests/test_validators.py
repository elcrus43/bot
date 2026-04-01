# Тесты для валидации
# Запуск: pytest tests/test_validators.py -v

import pytest
from handlers_new import is_valid_phone, is_valid_name


class TestPhoneValidation:
    """Тесты валидации телефона."""
    
    def test_valid_phone_with_plus(self):
        assert is_valid_phone("+7 (999) 123-45-67") is True
    
    def test_valid_phone_without_plus(self):
        assert is_valid_phone("89991234567") is True
    
    def test_valid_phone_international(self):
        assert is_valid_phone("+1 234 567 8901") is True
    
    def test_valid_phone_with_spaces(self):
        assert is_valid_phone("+7 999 123 45 67") is True
    
    def test_invalid_phone_too_short(self):
        assert is_valid_phone("123") is False
    
    def test_invalid_phone_letters(self):
        assert is_valid_phone("abc123") is False
    
    def test_invalid_phone_special_chars(self):
        assert is_valid_phone("@username") is False
    
    def test_invalid_phone_empty(self):
        assert is_valid_phone("") is False
    
    def test_invalid_phone_too_long(self):
        assert is_valid_phone("+7" + "1" * 20) is False


class TestNameValidation:
    """Тесты валидации имени."""
    
    def test_valid_name_russian(self):
        assert is_valid_name("Иван") is True
    
    def test_valid_name_english(self):
        assert is_valid_name("John") is True
    
    def test_valid_name_double(self):
        assert is_valid_name("Анна-Мария") is True
    
    def test_valid_name_with_space(self):
        assert is_valid_name("Сергей Иванович") is True
    
    def test_invalid_name_too_short(self):
        assert is_valid_name("A") is False
    
    def test_invalid_name_numbers(self):
        assert is_valid_name("123") is False
    
    def test_invalid_name_special_chars(self):
        assert is_valid_name("@user") is False
    
    def test_invalid_name_empty(self):
        assert is_valid_name("") is False
    
    def test_invalid_name_too_long(self):
        assert is_valid_name("A" * 100) is False
    
    def test_invalid_name_emoji(self):
        assert is_valid_name("Иван 😊") is False
