from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os
from database import save_lead, save_message, get_lead_by_telegram_id, get_messages_for_lead
from ai import get_ai_response
from dotenv import load_dotenv

import logging
load_dotenv()

logger = logging.getLogger(__name__)

router = Router()
REALTOR_ID = os.getenv("REALTOR_TELEGRAM_ID")


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

        await save_lead(
            telegram_id=user.id,
            username=user.username or "",
            full_name=full_name
        )

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
        "🏡 <b>Что я умею:</b>\n\n"
        "• Консультировать по покупке, продаже и аренде\n"
        "• Отвечать на вопросы о рынке недвижимости\n"
        "• Помочь определиться с бюджетом и районом\n"
        "• Связать вас с риэлтором\n\n"
        "Просто напишите ваш вопрос или выберите тему:",
        reply_markup=main_keyboard(),
        parse_mode="HTML"
    )


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

    await callback.message.edit_text(reply_text)
    await callback.answer()


@router.callback_query(F.data == "leave_contact")
async def handle_leave_contact(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "📞 Отлично! Чтобы риэлтор мог с вами связаться, укажите ваш номер телефона:"
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
    await state.update_data(phone=phone)
    await state.set_state(LeadForm.collecting_name)
    await message.answer("✅ Отлично! Теперь укажите ваше имя:")


@router.message(LeadForm.collecting_name)
async def process_name(message: Message, state: FSMContext):
    data = await state.get_data()
    phone = data.get("phone")
    name = message.text.strip()
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
            await message.bot.send_message(
                chat_id=int(REALTOR_ID),
                text=f"🔔 <b>Новый лид!</b>\n\n"
                     f"👤 Имя: {name}\n"
                     f"📞 Телефон: {phone}\n"
                     f"🆔 Telegram: @{user.username or 'нет'}\n"
                     f"🏠 Интерес: {lead.get('interest', 'не указан') if lead else 'не указан'}",
                parse_mode="HTML"
            )
        except Exception:
            pass


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

        history = await get_messages_for_lead(lead["id"])

        await message.bot.send_chat_action(message.chat.id, "typing")

        ai_reply = await get_ai_response(message.text, history)

        await save_message(lead["id"], "assistant", ai_reply)

        # Каждые 3 сообщения предлагаем оставить контакт
        msg_count = len(history)
        if msg_count > 0 and msg_count % 3 == 0:
            await message.answer(ai_reply, reply_markup=contact_keyboard())
        else:
            await message.answer(ai_reply)
    except Exception as e:
        logger.exception(f"Error in handle_message: {e}")
        await message.answer("Извините, произошла ошибка. Пожалуйста, повторите попытку позже.")
