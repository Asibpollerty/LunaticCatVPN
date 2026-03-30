from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from config import VPN_SERVERS, CHANNEL_ID

def main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="🔑 Получить ключ"),
        KeyboardButton(text="🌍 Серверы")
    )
    builder.row(
        KeyboardButton(text="👤 Профиль"),
        KeyboardButton(text="📋 Мои ключи")
    )
    builder.row(
        KeyboardButton(text="👑 Купить Premium"),
        KeyboardButton(text="🆘 Поддержка")
    )
    return builder.as_markup(resize_keyboard=True)

def servers_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    load_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}
    
    for server_name, data in VPN_SERVERS.items():
        load = load_emoji.get(data["load"], "⚪")
        builder.row(
            InlineKeyboardButton(
                text=f"{data['flag']} {data['city']} {load} {data['ping']}",
                callback_data=f"server:{server_name}"
            )
        )
    
    builder.row(
        InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh_servers")
    )
    return builder.as_markup()

def get_key_keyboard(server_name: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="✅ Получить ключ",
            callback_data=f"getkey:{server_name}"
        )
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Назад", callback_data="back_servers")
    )
    return builder.as_markup()

def key_actions_keyboard(key_value: str, server_url: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="❓ Как подключиться?",
            callback_data="howto"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="🔑 Получить ещё ключ",
            callback_data="get_another_key"
        )
    )
    return builder.as_markup()

def subscribe_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="📢 Подписаться на канал",
            url=f"https://t.me/{CHANNEL_ID.lstrip('@')}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="✅ Я подписался",
            callback_data="check_sub"
        )
    )
    return builder.as_markup()

def support_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="💬 Написать в поддержку",
            url="https://t.me/lunaticcat_support"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="📖 FAQ",
            callback_data="faq"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="🔧 Как настроить VPN?",
            callback_data="howto"
        )
    )
    return builder.as_markup()

def admin_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
        InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast")
    )
    builder.row(
        InlineKeyboardButton(text="👑 Выдать Premium", callback_data="admin_premium"),
        InlineKeyboardButton(text="🚫 Бан", callback_data="admin_ban")
    )
    builder.row(
        InlineKeyboardButton(text="📋 Список юзеров", callback_data="admin_users")
    )
    return builder.as_markup()