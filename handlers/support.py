from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import support_keyboard

router = Router()

@router.message(F.text == "🆘 Поддержка")
@router.message(Command("support"))
async def support_menu(message: Message):
    support_text = """
<b>🆘 Поддержка LunaticCatVPN</b>

━━━━━━━━━━━━━━━━━━━━━━
Мы готовы помочь тебе!
━━━━━━━━━━━━━━━━━━━━━━

📞 <b>Способы связи:</b>
• 💬 Написать в @lunaticcat_support
• 📧 support@lunaticcat.vpn

⏰ <b>Время ответа:</b> до 24 часов

<b>🔧 Частые проблемы:</b>
• Ключ не работает → попробуй другой сервер
• Медленная скорость → выбери 🟢 сервер
• Ошибка подключения → проверь приложение

<i>Нажми кнопку ниже для быстрой помощи</i>
    """
    
    await message.answer(support_text, reply_markup=support_keyboard())