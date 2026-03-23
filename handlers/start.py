from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from database import register_user, get_user
from keyboards import main_keyboard, subscribe_keyboard
from config import CHANNEL_ID, ADMIN_IDS
import logging

router = Router()

WELCOME_TEXT = """
<b>😺 Добро пожаловать в LunaticCatVPN!</b>

╔═══════════════════════╗
║  🐱 <b>LunaticCat VPN</b>        ║
║  Твой безопасный интернет   ║
╚═══════════════════════╝

🌟 <b>Что умеет наш бот?</b>

🔑 <b>Бесплатные ключи</b> — каждый день
🌍 <b>5 серверов</b> по всему миру  
⚡️ <b>Высокая скорость</b> соединения
🔒 <b>Полная анонимность</b>
📱 <b>Работает</b> на всех устройствах

━━━━━━━━━━━━━━━━━━━━━━
<i>🐾 Нажми кнопку ниже и начни пользоваться!</i>
"""

SUBSCRIBE_TEXT = """
<b>😿 Упс! Нужна подписка</b>

Для использования <b>LunaticCatVPN</b> необходимо 
подписаться на наш канал.

📢 Там мы публикуем:
• 🆕 Новые серверы и ключи
• 📰 Новости VPN
• 🎁 Промокоды и акции
• 🛠 Обновления бота

<i>Подпишись и возвращайся!</i> 🐱
"""

@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    user = message.from_user
    
    args = message.text.split()
    ref_by = None
    if len(args) > 1:
        try:
            ref_by = int(args[1])
            if ref_by == user.id:
                ref_by = None
        except ValueError:
            pass
    
    register_user(user.id, user.username or "", user.first_name, ref_by)
    
    is_subscribed = await check_subscription(bot, user.id)
    
    if not is_subscribed:
        await message.answer(
            SUBSCRIBE_TEXT,
            reply_markup=subscribe_keyboard()
        )
        return
    
    await message.answer_animation(
        animation="https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif",
        caption=WELCOME_TEXT,
        reply_markup=main_keyboard()
    )
    
    logging.info(f"👤 Новый пользователь: {user.id} | @{user.username}")

@router.callback_query(F.data == "check_sub")
async def check_sub_callback(callback: CallbackQuery, bot: Bot):
    is_subscribed = await check_subscription(bot, callback.from_user.id)
    
    if is_subscribed:
        await callback.message.delete()
        await callback.message.answer(
            WELCOME_TEXT,
            reply_markup=main_keyboard()
        )
        await callback.answer("✅ Отлично! Добро пожаловать!", show_alert=True)
    else:
        await callback.answer(
            "❌ Вы ещё не подписались на канал!",
            show_alert=True
        )

async def check_subscription(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status not in ["left", "kicked"]
    except Exception:
        return True  # если канал не задан — пускаем всех

@router.message(Command("help"))
async def cmd_help(message: Message):
    help_text = """
<b>🐱 LunaticCatVPN — Помощь</b>

<b>📌 Основные команды:</b>
/start — Главное меню
/key — Получить VPN ключ
/servers — Список серверов
/profile — Мой профиль
/help — Помощь

<b>🔑 Как получить ключ:</b>
1️⃣ Выбери сервер в меню «Серверы»
2️⃣ Нажми «Получить ключ»
3️⃣ Скопируй ключ и вставь в приложение

<b>📱 Поддерживаемые приложения:</b>
• V2rayNG (Android)
• V2Box (iOS)  
• Hiddify (Windows/Mac)

<b>⏱ Лимиты:</b>
• Бесплатно: 1 ключ в день
• Premium: неограниченно

<i>По вопросам: @lunaticcat_support</i>
    """
    await message.answer(help_text)