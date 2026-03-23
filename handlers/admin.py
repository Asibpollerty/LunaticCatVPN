from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import get_stats, get_all_users, ban_user, set_premium
from keyboards import admin_keyboard
from config import ADMIN_IDS
import asyncio
import logging

router = Router()

class AdminStates(StatesGroup):
    broadcast = State()
    set_premium = State()
    ban_user = State()

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Нет доступа")
        return
    
    await message.answer(
        "<b>🛡 Панель администратора</b>\n\n"
        "Выбери действие:",
        reply_markup=admin_keyboard()
    )

@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    
    total_users, total_keys, premium_users, new_today = get_stats()
    
    stats_text = f"""
<b>📊 Статистика LunaticCatVPN</b>

━━━━━━━━━━━━━━━━━━━━━━
👥 <b>Всего пользователей:</b> {total_users}
🆕 <b>Новых сегодня:</b> {new_today}
👑 <b>Premium пользователей:</b> {premium_users}
🔑 <b>Выдано ключей:</b> {total_keys}
━━━━━━━━━━━━━━━━━━━━━━
    """
    
    await callback.message.edit_text(stats_text, reply_markup=admin_keyboard())
    await callback.answer()

@router.callback_query(F.data == "admin_broadcast")
async def admin_broadcast_start(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    
    await callback.message.answer("✏️ Введи текст для рассылки:")
    await state.set_state(AdminStates.broadcast)
    await callback.answer()

@router.message(AdminStates.broadcast)
async def do_broadcast(message: Message, state: FSMContext, bot: Bot):
    users = get_all_users()
    success = 0
    failed = 0
    
    status_msg = await message.answer(f"📢 Начинаю рассылку для {len(users)} пользователей...")
    
    for user_id in users:
        try:
            await bot.send_message(user_id, message.text, parse_mode="HTML")
            success += 1
            await asyncio.sleep(0.05)
        except Exception:
            failed += 1
    
    await status_msg.edit_text(
        f"✅ Рассылка завершена!\n\n"
        f"✅ Успешно: {success}\n"
        f"❌ Ошибок: {failed}"
    )
    await state.clear()

@router.callback_query(F.data == "admin_premium")
async def admin_set_premium(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    
    await callback.message.answer("👑 Введи ID пользователя для выдачи Premium:")
    await state.set_state(AdminStates.set_premium)
    await callback.answer()

@router.message(AdminStates.set_premium)
async def do_set_premium(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = int(message.text.strip())
        set_premium(user_id, True)
        await message.answer(f"✅ Premium выдан пользователю {user_id}")
        await bot.send_message(
            user_id,
            "🎉 <b>Поздравляем!</b>\n\n"
            "Тебе выдан <b>👑 Premium</b> доступ!\n"
            "Теперь ты можешь получать неограниченное количество ключей!"
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
    
    await state.clear()

@router.callback_query(F.data == "admin_ban")
async def admin_ban(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    
    await callback.message.answer("🚫 Введи ID пользователя для бана:")
    await state.set_state(AdminStates.ban_user)
    await callback.answer()

@router.message(AdminStates.ban_user)
async def do_ban(message: Message, state: FSMContext):
    try:
        user_id = int(message.text.strip())
        ban_user(user_id)
        await message.answer(f"✅ Пользователь {user_id} заблокирован")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
    
    await state.clear()