from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import set_premium, get_user
import aiohttp
import os
import logging

router = Router()

CRYPTO_TOKEN = os.getenv("CRYPTO_TOKEN", "")


@router.message(F.text == "👑 Купить Premium")
async def buy_premium(message: Message):
    text = """
<b>👑 Premium LunaticCatVPN</b>

━━━━━━━━━━━━━━━━━━━━━━

<b>Что даёт Premium:</b>
✅ Безлимитные ключи
✅ Все серверы доступны
✅ Приоритетная поддержка
✅ Без рекламы

━━━━━━━━━━━━━━━━━━━━━━

<b>💰 Цены:</b>
• 7 дней — <b>1 USDT</b>
• 30 дней — <b>3 USDT</b>
• 90 дней — <b>7 USDT</b>

━━━━━━━━━━━━━━━━━━━━━━
<i>Оплата через CryptoBot (USDT, TON, BTC)</i>
    """

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="⭐ 7 дней — 1 USDT",
            callback_data="pay:7:1"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="👑 30 дней — 3 USDT",
            callback_data="pay:30:3"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="💎 90 дней — 7 USDT",
            callback_data="pay:90:7"
        )
    )

    await message.answer(text, reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("pay:"))
async def process_payment(callback: CallbackQuery):
    parts = callback.data.split(":")
    days = parts[1]
    amount = parts[2]

    invoice_url = await create_invoice(amount, days, callback.from_user.id)

    if not invoice_url:
        await callback.answer("❌ Ошибка создания платежа", show_alert=True)
        return

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=f"💳 Оплатить {amount} USDT",
            url=invoice_url
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="✅ Я оплатил",
            callback_data=f"check_pay:{days}"
        )
    )

    await callback.message.answer(
        f"<b>💳 Оплата Premium на {days} дней</b>\n\n"
        f"Сумма: <b>{amount} USDT</b>\n\n"
        f"Нажми кнопку ниже для оплаты через CryptoBot:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("check_pay:"))
async def check_payment(callback: CallbackQuery):
    days = callback.data.split(":")[1]

    paid = await check_invoices(callback.from_user.id)

    if paid:
        set_premium(callback.from_user.id, True)
        await callback.message.answer(
            f"🎉 <b>Оплата прошла!</b>\n\n"
            f"Тебе выдан 👑 <b>Premium</b> на {days} дней!\n"
            f"Теперь ключи безлимитно!"
        )
        await callback.answer("✅ Premium активирован!", show_alert=True)
    else:
        await callback.answer(
            "❌ Оплата не найдена! Попробуй позже.",
            show_alert=True
        )


async def create_invoice(amount: str, days: str, user_id: int) -> str:
    try:
        url = "https://pay.crypt.bot/api/createInvoice"
        headers = {"Crypto-Pay-API-Token": CRYPTO_TOKEN}
        data = {
            "currency_type": "crypto",
            "asset": "USDT",
            "amount": amount,
            "description": f"Premium LunaticCatVPN {days} days",
            "hidden_message": f"Premium for user {user_id}",
            "paid_btn_name": "callback",
            "paid_btn_url": "https://t.me/LunaticCatVPNoffical_bot",
            "payload": f"{user_id}:{days}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as resp:
                result = await resp.json()
                if result.get("ok"):
                    return result["result"]["bot_invoice_url"]
                else:
                    logging.error(f"CryptoBot error: {result}")
                    return None
    except Exception as e:
        logging.error(f"Invoice error: {e}")
        return None


async def check_invoices(user_id: int) -> bool:
    try:
        url = "https://pay.crypt.bot/api/getInvoices"
        headers = {"Crypto-Pay-API-Token": CRYPTO_TOKEN}
        params = {"status": "paid"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                result = await resp.json()
                if result.get("ok"):
                    for invoice in result["result"]["items"]:
                        payload = invoice.get("payload", "")
                        if str(user_id) in payload:
                            return True
                return False
    except Exception as e:
        logging.error(f"Check payment error: {e}")
        return False