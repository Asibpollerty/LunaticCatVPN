from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.deep_linking import create_start_link
from database import get_user, get_user_keys
from keyboards import main_keyboard
from config import ADMIN_IDS

router = Router()

@router.message(F.text == "👤 Профиль")
@router.message(Command("profile"))
async def show_profile(message: Message, bot):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if not user:
        await message.answer("❌ Профиль не найден. Напиши /start")
        return
    
    (uid, username, first_name, joined_at, is_banned, 
     is_premium, keys_today, last_key_date, total_keys, 
     referrals, ref_by) = user
    
    status = "👑 Premium" if is_premium else "🆓 Free"
    admin_badge = "🛡 Admin | " if user_id in ADMIN_IDS else ""
    
    ref_link = await create_start_link(bot, str(user_id))
    
    profile_text = f"""
<b>🐱 Профиль LunaticCatVPN</b>

╔═══════════════════════╗
║ {admin_badge}{status}
╚═══════════════════════╝

👤 <b>Имя:</b> {first_name}
🆔 <b>ID:</b> <code>{user_id}</code>
📅 <b>Дата регистрации:</b> {joined_at[:10]}

━━━━━━━━━━━━━━━━━━━━━━

🔑 <b>Ключей сегодня:</b> {keys_today}/{"∞" if is_premium else "1"}
📊 <b>Всего ключей:</b> {total_keys}
👥 <b>Рефералов:</b> {referrals}

━━━━━━━━━━━━━━━━━━━━━━

🔗 <b>Твоя реф. ссылка:</b>
<code>{ref_link}</code>

<i>Приглашай друзей и получай бонусы!</i>
    """
    
    await message.answer(profile_text)

@router.message(F.text == "📋 Мои ключи")
@router.message(Command("mykeys"))
async def show_my_keys(message: Message):
    user_id = message.from_user.id
    keys = get_user_keys(user_id)
    
    if not keys:
        await message.answer(
            "😿 <b>У тебя пока нет ключей</b>\n\n"
            "Нажми «🔑 Получить ключ» чтобы начать!"
        )
        return
    
    text = "<b>📋 Твои последние ключи:</b>\n\n"
    
    for i, (server_name, key_value, created_at, expires_at, is_active) in enumerate(keys, 1):
        status_icon = "🟢" if is_active else "🔴"
        short_key = key_value[:40] + "..." if len(key_value) > 40 else key_value
        
        text += (
            f"{i}. {status_icon} <b>{server_name}</b>\n"
            f"   📅 {created_at[:16]}\n"
            f"   ⏱ До: {expires_at[:16]}\n"
            f"   🔑 <code>{short_key}</code>\n\n"
        )
    
    await message.answer(text)

@router.message(F.text == "👥 Рефералы")
async def show_referrals(message: Message, bot):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if not user:
        return
    
    referrals = user[9]
    ref_link = await create_start_link(bot, str(user_id))
    
    ref_text = f"""
<b>👥 Реферальная программа</b>

━━━━━━━━━━━━━━━━━━━━━━
📊 <b>Твои рефералы:</b> {referrals} чел.
━━━━━━━━━━━━━━━━━━━━━━

🎁 <b>Бонусы за рефералов:</b>
• 3 реферала → +1 ключ в день
• 10 рефералов → Premium на 7 дней
• 25 рефералов → Premium на 30 дней

🔗 <b>Твоя ссылка:</b>
<code>{ref_link}</code>

<i>Поделись ссылкой с друзьями!</i>
    """
    
    await message.answer(ref_text)