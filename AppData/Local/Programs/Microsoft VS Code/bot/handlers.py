import re
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from middleware import RateLimitMiddleware
import os
from database import save_lead, save_message, get_lead_by_telegram_id, get_messages_for_lead, get_stats, count_leads
from ai import get_ai_response
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)
router = Router()

# Конфигурация
REALTOR_ID = os.getenv("REALTOR_TELEGRAM_ID")
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "20"))

# Паттерны валидации
PHONE_PATTERN = re.compile(r'^[\d\+\-\(\)\s]{10,20}$')
NAME_PATTERN = re.compile(r'^[а-яА-Яa-zA-Z\s\-]{2,50}$')


def is_valid_phone(phone: str) -> bool:
    """Валидация номера телефона."""
    digits = re.sub(r'\D', '', phone)
    return 10 <= len(digits) <= 15


def is_valid_name(name: str) -> bool:
    """Валидация имени."""
    return bool(NAME_PATTERN.match(name)) and len(name.strip()) >= 2


# Rate limiting middleware (1 сообщение в 3 секунды)
router.message.middleware(RateLimitMiddleware(limit=3.0))


class LeadForm(StatesGroup):
    collecting_phone = State()
    collecting_name = State()


def main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🏠 Купить квартиру", callback_data="interest_buy")
    builder.button(text="💰 Продать недвижимость", callback_data="interest_sell")
    builder.button(text="🔑 Снять жильё", callback_data="interest_rent")
    builder.button(text="📞 Оставить заявку", callback_data="leave_contact")
    builder.adjust(2)
    return builder.as_markup()


def contact_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="📞 Оставить контакт", callback_data="leave_contact")
    builder.button(text="💬 Продолжить диалог", callback_data="continue_chat")
    builder.adjust(1)
    return builder.as_markup()


@router.message(CommandStart())
async def cmd_start(message: Message):
    try:
        user = message.from_user
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        lead = await save_lead(
            telegram_id=user.id,
            username=user.username or "",
            full_name=full_name
        )
        if lead:
            logger.info(f"New lead started: {user.id} ({full_name})")
        
        await message.answer(
            f"👋 Здравствуйте, {user.first_name}!\n\n"
            "Я — AI-ассистент агентства недвижимости. Помогу вам:\n"
            "• Найти квартиру или дом для покупки\n"
            "• Продать вашу недвижимость выгодно\n"
            "• Подобрать жильё в аренду\n\n"
            "Выберите, что вас интересует, или напишите свой вопрос:",
            reply_markup=main_keyboard()
        )
    except Exception as e:
        logger.exception(f"Error in cmd_start: {e}")
        await message.answer("Произошла ошибка при запуске бота. Попробуйте еще раз.")


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "🏡 Что я умею:\n\n"
        "• Консультировать по покупке, продаже и аренде\n"
        "• Отвечать на вопросы о рынке недвижимости\n"
        "• Помочь определиться с бюджетом и районом\n"
        "• Связать вас с риэлтором\n\n"
        "Просто напишите ваш вопрос или выберите тему:",
        reply_markup=main_keyboard(),
        parse_mode="HTML"
    )


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Админ команда: статистика бота."""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ У вас нет прав для просмотра статистики.")
        return
    
    try:
        stats = await get_stats()
        total_leads = await count_leads()
        
        await message.answer(
            "📊 <b>Статистика бота</b>\n\n"
            f"• Всего лидов: {total_leads}\n"
            f"• Лидов за 24ч: {stats.get('leads_24h', 0)}\n"
            f"• Сообщений за 24ч: {stats.get('messages_24h', 0)}\n"
            f"• Среднее время ответа: {stats.get('avg_response_time', 'N/A')} сек\n\n"
            f"<b>Популярные интересы:</b>\n"
            f"• Купить: {stats.get('interest_buy', 0)}\n"
            f"• Продать: {stats.get('interest_sell', 0)}\n"
            f"• Арендовать: {stats.get('interest_rent', 0)}",
            parse_mode="HTML"
        )
    except Exception as e:
        logger.exception(f"Error in cmd_stats: {e}")
        await message.answer("❌ Ошибка при получении статистики.")


@router.message(Command("health"))
async def cmd_health(message: Message):
    """Админ команда: проверка здоровья бота."""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ У вас нет прав для этой команды.")
        return

    try:
        from ai import check_siliconflow_health
        api_status = await check_siliconflow_health()
        
        status = "✅ Бот работает нормально" if api_status else "⚠️ SiliconFlow API недоступен"
        
        await message.answer(
            f"🏥 <b>Health Check</b>\n\n"
            f"• Статус: {status}\n"
            f"• SiliconFlow API: {'✅ OK' if api_status else '❌ ERROR'}\n"
            f"• База данных: ✅ OK\n"
            f"• Telegram API: ✅ OK",
            parse_mode="HTML"
        )
    except Exception as e:
        logger.exception(f"Error in cmd_health: {e}")
        await message.answer("❌ Ошибка при проверке здоровья бота.")


@router.callback_query(F.data.startswith("interest_"))
async def handle_interest(callback: CallbackQuery):
    interest_map = {
        "interest_buy": ("купить", "🏠 Вы хотите купить недвижимость. Отличный выбор!\n\nРасскажите подробнее: какой район вас интересует и какой у вас примерный бюджет?"),
        "interest_sell": ("продать", "💰 Вы хотите продать недвижимость. Помогу оценить и найти покупателей!\n\nРасскажите: что именно продаёте и в каком районе объект?"),
        "interest_rent": ("аренда", "🔑 Ищете жильё в аренду. Подберём лучшие варианты!\n\nУточните: какой район предпочитаете и какой ежемесячный бюджет?"),
    }
    interest_key = callback.data
    interest_type, reply_text = interest_map.get(interest_key, ("другое", "Расскажите подробнее о вашем запросе:"))
    
    user = callback.from_user
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    lead = await save_lead(
        telegram_id=user.id,
        username=user.username or "",
        full_name=full_name,
        interest=interest_type
    )
    if lead:
        await save_message(lead["id"], "assistant", reply_text)
        logger.info(f"User {user.id} selected interest: {interest_type}")
        await callback.message.edit_text(reply_text)
        await callback.answer()


@router.callback_query(F.data == "leave_contact")
async def handle_leave_contact(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "📞 Отлично! Чтобы риэлтор мог с вами связаться, укажите ваш номер телефона:\n\n"
        "Пример: +7 (999) 123-45-67 или 89991234567"
    )
    await state.set_state(LeadForm.collecting_phone)
    await callback.answer()


@router.callback_query(F.data == "continue_chat")
async def handle_continue_chat(callback: CallbackQuery):
    await callback.message.answer("Конечно! Задайте ваш вопрос:")
    await callback.answer()


@router.message(LeadForm.collecting_phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    
    if not is_valid_phone(phone):
        await message.answer(
            "❌ Пожалуйста, введите корректный номер телефона.\n\n"
            "Пример: +7 (999) 123-45-67 или 89991234567\n\n"
            "Попробуйте ещё раз:"
        )
        return
    
    await state.update_data(phone=phone)
    await state.set_state(LeadForm.collecting_name)
    await message.answer("✅ Отлично! Теперь укажите ваше имя:")


@router.message(LeadForm.collecting_name)
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()
    
    if not is_valid_name(name):
        await message.answer(
            "❌ Пожалуйста, введите корректное имя (2-50 символов, только буквы).\n\n"
            "Попробуйте ещё раз:"
        )
        return
    
    data = await state.get_data()
    phone = data.get("phone")
    user = message.from_user
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    
    lead = await save_lead(
        telegram_id=user.id,
        username=user.username or "",
        full_name=full_name,
        phone=phone,
        notes=f"Контактное имя: {name}"
    )
    await state.clear()
    
    await message.answer(
        f"🎉 Спасибо, {name}!\n\n"
        "Ваша заявка принята. Риэлтор свяжется с вами в ближайшее время.\n\n"
        "Если есть ещё вопросы — смело спрашивайте!",
        reply_markup=main_keyboard()
    )
    
    # Уведомление риэлтору
    if REALTOR_ID:
        try:
            realtor_chat_id = int(REALTOR_ID)
            await message.bot.send_message(
                chat_id=realtor_chat_id,
                text=(
                    f"🔔 <b>Новый лид!</b>\n\n"
                    f"👤 Имя: {name}\n"
                    f"📞 Телефон: {phone}\n"
                    f"🆔 Telegram: @{user.username or 'нет'}\n"
                    f"🏠 Интерес: {lead.get('interest', 'не указан') if lead else 'не указан'}"
                ),
                parse_mode="HTML"
            )
            logger.info(f"Lead notification sent to realtor {realtor_chat_id}")
        except ValueError as e:
            logger.error(f"Invalid REALTOR_ID format: {REALTOR_ID}. Error: {e}")
        except Exception as e:
            logger.exception(f"Failed to send lead notification: {e}")


@router.message()
async def handle_message(message: Message):
    """Обработка обычных сообщений через Groq AI"""
    try:
        user = message.from_user
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        
        lead = await get_lead_by_telegram_id(user.id)
        if not lead:
            lead = await save_lead(
                telegram_id=user.id,
                username=user.username or "",
                full_name=full_name
            )
        
        if not lead:
            await message.answer("Произошла ошибка (не удалось создать лид). Попробуйте /start")
            return
        
        await save_message(lead["id"], "user", message.text)
        history = await get_messages_for_lead(lead["id"], limit=MAX_HISTORY_MESSAGES)
        
        await message.bot.send_chat_action(message.chat.id, "typing")
        ai_reply = await get_ai_response(message.text, history)
        await save_message(lead["id"], "assistant", ai_reply)
        
        # Каждые 3 сообщения предлагаем оставить контакт
        msg_count = len(history)
        if msg_count > 0 and msg_count % 3 == 0:
            await message.answer(ai_reply, reply_markup=contact_keyboard())
        else:
            await message.answer(ai_reply)
            
        logger.debug(f"AI response generated for user {user.id}")
        
    except Exception as e:
        logger.exception(f"Error in handle_message: {e}")
        await message.answer("Извините, произошла ошибка. Пожалуйста, повторите попытку позже.")
