from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database import can_get_key, save_key
from keyboards import (
    servers_keyboard, get_key_keyboard,
    key_actions_keyboard
)
from config import VPN_SERVERS
import logging

router = Router()

SERVERS_TEXT = """
<b>🌍 Доступные серверы LunaticCatVPN</b>

╔══════════════════════╗
║ 🟢 Низкая нагрузка        ║
║ 🟡 Средняя нагрузка       ║
║ 🔴 Высокая нагрузка       ║
╚══════════════════════╝

<b>Выбери сервер для подключения:</b>
"""

NO_KEY_TEXT = """
<b>😿 Лимит исчерпан</b>

Ты уже получил бесплатный ключ сегодня.

⏰ <b>Новый ключ будет доступен:</b>
через <b>24 часа</b> с момента последнего получения

💎 <b>Хочешь неограниченный доступ?</b>
Получи <b>Premium</b> и пользуйся без ограничений!

Обратись к @lunaticcat_support для покупки Premium
"""

HOWTO_TEXT = """
<b>🔧 Как подключиться к VPN?</b>

━━━━━━━━━━━━━━━━━━━━━━

<b>📱 Android:</b>
1. Скачай <b>V2rayNG</b> из Play Market
2. Нажми ➕ → «Import from URL»
3. Вставь полученный ключ
4. Нажми ▶️ для подключения

<b>🍎 iOS:</b>
1. Скачай <b>V2Box</b> из App Store
2. Нажми «+» → «Import»
3. Вставь ключ в поле
4. Подключайся!

<b>💻 Windows / macOS:</b>
1. Скачай <b>Hiddify</b>
2. Нажми «Добавить профиль»
3. Вставь ссылку с ключом
4. Нажми «Подключить»

━━━━━━━━━━━━━━━━━━━━━━
<i>🆘 Остались вопросы? @lunaticcat_support</i>
"""

FAQ_TEXT = """
<b>❓ Часто задаваемые вопросы</b>

━━━━━━━━━━━━━━━━━━━━━━

<b>🔸 Ключ не работает?</b>
Попробуй другой се��вер или дождись обновления ключа.

<b>🔸 Медленная скорость?</b>
Выбери сервер с низкой нагрузкой (🟢).

<b>🔸 Можно использовать на нескольких устройствах?</b>
Да, ключ работает одновременно на 3 устройствах.

<b>🔸 Как получить Premium?</b>
Напиши нам: @lunaticcat_support

<b>🔸 Зачем нужна подписка на канал?</b>
Там выходят важные обновления и новые серверы.

━━━━━━━━━━━━━━━━━━━━━━
"""


@router.message(F.text == "🌍 Серверы")
@router.message(Command("servers"))
async def show_servers(message: Message):
    await message.answer(
        SERVERS_TEXT,
        reply_markup=servers_keyboard()
    )


@router.message(F.text == "🔑 Получить ключ")
@router.message(Command("key"))
async def get_key_menu(message: Message):
    await message.answer(
        SERVERS_TEXT,
        reply_markup=servers_keyboard()
    )


@router.callback_query(F.data == "refresh_servers")
async def refresh_servers(callback: CallbackQuery):
    await callback.message.edit_text(
        SERVERS_TEXT,
        reply_markup=servers_keyboard()
    )
    await callback.answer("🔄 Обновлено!")


@router.callback_query(F.data.startswith("server:"))
async def server_info(callback: CallbackQuery):
    server_name = callback.data.split(":", 1)[1]
    server = VPN_SERVERS.get(server_name)

    if not server:
        await callback.answer("❌ Сервер не найден")
        return

    load_text = {
        "low": "🟢 Низкая",
        "medium": "🟡 Средняя",
        "high": "🔴 Высокая"
    }

    text = f"""
<b>{server['flag']} Сервер: {server['city']}, {server['country']}</b>

━━━━━━━━━━━━━━━━━━━━━━
🏙 <b>Город:</b> {server['city']}
📡 <b>Пинг:</b> {server['ping']}
📊 <b>Нагрузка:</b> {load_text.get(server['load'], '⚪ Неизвестно')}
🔒 <b>Протокол:</b> Shadowsocks
━━━━━━━━━━━━━━━━━━━━━━

<i>Нажми кнопку ниже, чтобы получить ключ</i> 🔑
    """

    await callback.message.edit_text(
        text,
        reply_markup=get_key_keyboard(server_name)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("getkey:"))
async def generate_key(callback: CallbackQuery):
    user_id = callback.from_user.id
    server_name = callback.data.split(":", 1)[1]
    server = VPN_SERVERS.get(server_name)

    if not server:
        await callback.answer("❌ Сервер не найден", show_alert=True)
        return

    if not can_get_key(user_id):
        await callback.message.answer(NO_KEY_TEXT)
        await callback.answer("😿 Лимит исчерпан", show_alert=True)
        return

    await callback.answer("✅ Ключ готов!")

    key_value = server.get("key", "")

    save_key(user_id, server_name, key_value, key_value)

    success_text = f"""
<b>🎉 Ключ успешно получен!</b>

╔══════════════════════╗
║ 🐱 <b>LunaticCat VPN</b>         ║
║ {server['flag']} {server['city']}, {server['country']}
╚══════════════════════╝

<b>🔑 Твой VPN ключ:</b>
<code>{key_value}</code>

━━━━━━━━━━━━━━━━━━━━━━
📡 <b>Сервер:</b> {server['city']}
⚡️ <b>Пинг:</b> {server['ping']}
⏱ <b>Действует:</b> 24 часа
━━━━━━━━━━━━━━━━━━━━━━

<i>Нажми на ключ чтобы скопировать!</i>
    """

    await callback.message.answer(
        success_text,
        reply_markup=key_actions_keyboard(key_value, key_value)
    )


@router.callback_query(F.data == "back_servers")
async def back_to_servers(callback: CallbackQuery):
    await callback.message.edit_text(
        SERVERS_TEXT,
        reply_markup=servers_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "howto")
async def show_howto(callback: CallbackQuery):
    await callback.message.answer(HOWTO_TEXT)
    await callback.answer()


@router.callback_query(F.data == "faq")
async def show_faq(callback: CallbackQuery):
    await callback.message.answer(FAQ_TEXT)
    await callback.answer()


@router.callback_query(F.data == "get_another_key")
async def get_another_key(callback: CallbackQuery):
    await callback.message.answer(
        SERVERS_TEXT,
        reply_markup=servers_keyboard()
    )
    await callback.answer()