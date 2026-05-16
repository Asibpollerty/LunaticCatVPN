import asyncio
import os
import json
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ContentType,
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 1477975069

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

# ─── База данных (файл чтобы не терялась) ─

USERS_FILE = "users.json"
RATINGS_FILE = "ratings.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
            result = {}
            for k, v in raw.items():
                v["joined"] = datetime.fromisoformat(v["joined"])
                result[int(k)] = v
            return result
    return {}

def save_users():
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        serializable = {}
        for k, v in users.items():
            serializable[k] = {
                **v,
                "joined": v["joined"].isoformat()
            }
        json.dump(serializable, f, ensure_ascii=False, indent=2)

def load_ratings():
    if os.path.exists(RATINGS_FILE):
        with open(RATINGS_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
            return {int(k): v for k, v in raw.items()}
    return {}

def save_ratings():
    with open(RATINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(ratings, f, ensure_ascii=False, indent=2)

# Загружаем при старте
users = load_users()
ratings = load_ratings()
start_time = datetime.now()

# ─── Клавиатуры ───────────────────────────

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔑 Хочу ключик",
                callback_data="get_key"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Как там сервер?",
                callback_data="status"
            ),
            InlineKeyboardButton(
                text="👤 Мой профиль",
                callback_data="profile"
            ),
        ],
        [
            InlineKeyboardButton(
                text="📖 Инструкции",
                callback_data="instructions"
            ),
            InlineKeyboardButton(
                text="💬 Поддержка",
                callback_data="support"
            ),
        ],
        [
            InlineKeyboardButton(
                text="💳 Оплата",
                callback_data="payment"
            ),
        ],
        [
            InlineKeyboardButton(
                text="❓ FAQ",
                callback_data="faq"
            ),
            InlineKeyboardButton(
                text="💜 О проекте",
                callback_data="about"
            ),
        ]
    ]
)

admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📊 Статистика",
                callback_data="admin_stats"
            )
        ],
        [
            InlineKeyboardButton(
                text="👥 Наши пользователи",
                callback_data="admin_users"
            )
        ],
        [
            InlineKeyboardButton(
                text="⭐️ Рейтинг бота",
                callback_data="admin_ratings"
            )
        ],
        [
            InlineKeyboardButton(
                text="📢 Разослать опрос",
                callback_data="admin_send_survey"
            )
        ],
        [
            InlineKeyboardButton(
                text="Закрыть панель",
                callback_data="close"
            )
        ]
    ]
)

rating_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1 😞", callback_data="rate_1"),
            InlineKeyboardButton(text="2 😕", callback_data="rate_2"),
            InlineKeyboardButton(text="3 😐", callback_data="rate_3"),
            InlineKeyboardButton(text="4 😊", callback_data="rate_4"),
            InlineKeyboardButton(text="5 🔥", callback_data="rate_5"),
        ]
    ]
)

# ─── Задержанный запрос оценки ────────────

async def send_rating_request(user_id: int, first_name: str):
    """Через минуту после старта просим оценить бота."""
    await asyncio.sleep(60)
    try:
        await bot.send_message(
            user_id,
            f"Привет, <b>{first_name}</b>! 🐱\n\n"
            "Ты уже немного познакомился с нашим ботом.\n"
            "Мне очень важно твоё мнение — "
            "это поможет сделать сервис лучше.\n\n"
            "Как тебе <b>LunaicsCatsVPN</b>?\n"
            "Оцени от 1 до 5, пожалуйста 🙏",
            reply_markup=rating_menu
        )
    except Exception:
        # Пользователь мог заблокировать бота
        pass

# ─── Приветствие ──────────────────────────

@dp.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id
    is_new = user_id not in users

    if is_new:
        users[user_id] = {
            "username": message.from_user.username or "незнакомец",
            "first_name": message.from_user.first_name or "Друг",
            "joined": datetime.now()
        }
        save_users()

        # Уведомление админу
        await bot.send_message(
            ADMIN_ID,
            f"🐱 <b>Новый пользователь!</b>\n"
            f"Имя: {message.from_user.first_name}\n"
            f"Username: @{message.from_user.username or 'не указан'}\n"
            f"ID: <code>{user_id}</code>"
        )

        # Запускаем таймер — через минуту попросим оценить
        asyncio.create_task(
            send_rating_request(
                user_id,
                message.from_user.first_name or "друг"
            )
        )

    text = (
        f"Привет, <b>{message.from_user.first_name or 'дорогой друг'}</b>! 🐱\n\n"
        "Добро пожаловать в <b>LunaicsCatsVPN</b> — "
        "уютное место для свободного интернета.\n\n"
        "Мы только начинаем свой путь, поэтому "
        "не ругайся, если что-то пойдёт не так — "
        "я всё починю, обещаю! 💪\n\n"
        "<i>Сейчас мы в бета-тесте, так что "
        "ключи могут капризничать. Но ты "
        "всегда можешь написать мне в поддержку.</i>\n\n"
        "━━━━━━━━━━━━━━━━\n"
        "Что умеем:\n"
        "• WireGuard — быстрый и надёжный\n"
        "• Shadowsocks — лёгкий и простой\n"
        "━━━━━━━━━━━━━━━━\n\n"
        "<i>Выбирай, что по душе, и погнали!</i>"
    )

    await message.answer(text, reply_markup=main_menu)

# ─── Обработка оценки ─────────────────────

@dp.callback_query(F.data.startswith("rate_"))
async def handle_rating(callback: CallbackQuery):
    user = callback.from_user
    score = int(callback.data.split("_")[1])

    # Сохраняем оценку
    ratings[user.id] = {
        "score": score,
        "name": user.first_name or "Друг",
        "username": user.username or "не указан",
        "rated_at": datetime.now().isoformat()
    }
    save_ratings()

    # Считаем средний балл
    all_scores = [v["score"] for v in ratings.values()]
    avg = sum(all_scores) / len(all_scores)

    # Эмодзи по оценке
    emoji_map = {1: "😞", 2: "😕", 3: "😐", 4: "😊", 5: "🔥"}
    emoji = emoji_map[score]

    # Ответ пользователю
    if score >= 4:
        response = (
            f"{emoji} <b>Вау, спасибо!</b>\n\n"
            f"Ты поставил нам <b>{score} из 5</b> — "
            "это очень приятно!\n\n"
            "Мы стараемся для тебя и будем "
            "становиться только лучше 🐱💜"
        )
    elif score == 3:
        response = (
            f"{emoji} <b>Спасибо за честность!</b>\n\n"
            f"Ты поставил <b>{score} из 5</b>.\n\n"
            "Расскажи, что можно улучшить — "
            "напиши в поддержку (@sibpollerty), "
            "я обязательно прислушаюсь!"
        )
    else:
        response = (
            f"{emoji} <b>Спасибо, что не промолчал.</b>\n\n"
            f"Ты поставил <b>{score} из 5</b> — "
            "мне важно это знать.\n\n"
            "Напиши, что пошло не так — "
            "@sibpollerty. Я разберусь лично!"
        )

    await callback.message.edit_text(response)

    # Уведомление админу
    await bot.send_message(
        ADMIN_ID,
        f"⭐️ <b>Новая оценка!</b>\n\n"
        f"👤 {user.first_name}\n"
        f"💬 @{user.username or 'не указан'}\n"
        f"Оценка: <b>{score}/5 {emoji}</b>\n\n"
        f"📊 Средний балл: <b>{avg:.1f}/5</b> "
        f"(всего оценок: {len(all_scores)})"
    )

    await callback.answer()

# ─── Получение ключа ──────────────────────

@dp.callback_query(F.data == "get_key")
async def get_key(callback: CallbackQuery):
    text = (
        "🔑 <b>Выбирай протокол</b>\n\n"
        "Расскажу немного о каждом:\n\n"
        "⚡️ <b>WireGuard</b> — современный, "
        "шустрый, отлично подходит для "
        "повседневного использования.\n\n"
        "🦊 <b>Shadowsocks</b> — хитрый лис, "
        "маскируется под обычный трафик, "
        "идеален для обхода блокировок.\n\n"
        "<i>Какой тебе больше по душе?</i>"
    )

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⚡️ WireGuard",
                        callback_data="wg"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🦊 Shadowsocks",
                        callback_data="ss"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="↩️ Вернуться",
                        callback_data="back"
                    )
                ]
            ]
        )
    )
    await callback.answer()

@dp.callback_query(F.data.in_(["wg", "ss"]))
async def give_key(callback: CallbackQuery):
    protocol = "WireGuard" if callback.data == "wg" else "Shadowsocks"

    text = (
        f"🎉 <b>Твой {protocol} ключ готов!</b>\n\n"
        "Сейчас я сгенерирую для тебя "
        "персональный конфиг...\n\n"
        "<i>На самом деле, бот в разработке, "
        "и ключи пока виртуальные. Но совсем "
        "скоро здесь будет настоящая магия!</i>\n\n"
        "А пока можешь посмотреть инструкции "
        "по настройке или задать вопрос в поддержке."
    )

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📖 Как настроить",
                        callback_data="instructions"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="↩️ Назад",
                        callback_data="back"
                    )
                ]
            ]
        )
    )
    await callback.answer("Ключ почти готов!", show_alert=True)

# ─── Статус ───────────────────────────────

@dp.callback_query(F.data == "status")
async def status(callback: CallbackQuery):
    uptime = datetime.now() - start_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    text = (
        "📊 <b>Как поживает сервер</b>\n\n"
        "🟢 <b>Жив, здоров и работает!</b>\n\n"
        f"⏱ Не спим уже: <code>{days}д {hours}ч {minutes}м</code>\n"
        f"👥 Друзей в системе: <code>{len(users)}</code>\n\n"
        "<i>Сейчас мы в бета-режиме, "
        "так что всё очень нестабильно. "
        "Но я стараюсь!</i>"
    )

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔄 Обновить",
                        callback_data="status"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="↩️ Назад",
                        callback_data="back"
                    )
                ]
            ]
        )
    )
    await callback.answer()

# ─── Профиль ──────────────────────────────

@dp.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):
    user = callback.from_user
    user_data = users.get(user.id, {})
    joined = user_data.get("joined", datetime.now())
    days_with_us = (datetime.now() - joined).days

    # Оценка пользователя если есть
    user_rating = ratings.get(user.id)
    rating_text = (
        f"Твоя оценка: {'⭐️' * user_rating['score']}\n"
        if user_rating else
        "Оценка: ещё не оставил\n"
    )

    text = (
        "👤 <b>Твой уютный профиль</b>\n\n"
        f"Имя: <b>{user.first_name}</b>\n"
        f"Username: @{user.username or 'не указан'}\n"
        f"Твой ID: <code>{user.id}</code>\n\n"
        f"С нами уже: <b>{days_with_us} дней</b>\n"
        f"{rating_text}"
        "Статус: 🌟 Первопроходец\n\n"
        "<i>Спасибо, что ты с нами! "
        "Каждый пользователь для нас — "
        "не просто цифра, а целая история.</i>"
    )

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="↩️ Назад",
                        callback_data="back"
                    )
                ]
            ]
        )
    )
    await callback.answer()

# ─── Инструкции ───────────────────────────

@dp.callback_query(F.data == "instructions")
async def instructions(callback: CallbackQuery):
    text = (
        "📖 <b>Как подружиться с VPN</b>\n\n"
        "<b>⚡️ WireGuard:</b>\n"
        "1. Скачай приложение WireGuard\n"
        "   (есть на всё: iOS, Android, ПК)\n"
        "2. Нажми «Добавить туннель»\n"
        "3. Отсканируй QR-код или вставь конфиг\n"
        "4. Всё! Можно включать и пользоваться\n\n"
        "<b>🦊 Shadowsocks:</b>\n"
        "1. Установи клиент (например, Shadowrocket)\n"
        "2. Скопируй ссылку из бота\n"
        "3. Вставь в приложение\n"
        "4. Готово! Ты в интернете без границ\n\n"
        "<i>Если что-то не получается — "
        "не стесняйся, пиши в поддержку. "
        "Я помогу!</i>"
    )

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="↩️ Назад",
                        callback_data="back"
                    )
                ]
            ]
        )
    )
    await callback.answer()

# ─── Поддержка ────────────────────────────

@dp.callback_query(F.data == "support")
async def support(callback: CallbackQuery):
    text = (
        "💬 <b>Поддержка</b>\n\n"
        "Если что-то сломалось, не работает, "
        "или просто хочешь поболтать — "
        "я всегда рядом!\n\n"
        "Напиши мне в личку:\n"
        "@sibpollerty\n\n"
        "<i>Я стараюсь отвечать быстро, "
        "но иногда могу быть занят "
        "улучшением сервиса. Не обижайся, "
        "если ответ придёт не сразу!</i>\n\n"
        "🐱 Спасибо, что помогаешь "
        "нам становиться лучше!"
    )

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📝 Оставить обращение",
                        callback_data="ticket"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="↩️ Назад",
                        callback_data="back"
                    )
                ]
            ]
        )
    )
    await callback.answer()

@dp.callback_query(F.data == "ticket")
async def ticket(callback: CallbackQuery):
    text = (
        "📝 <b>Новое обращение</b>\n\n"
        "Опиши свою проблему или вопрос "
        "прямо здесь, в чате. "
        "Я передам его администратору, "
        "и он свяжется с тобой в ближайшее время.\n\n"
        "<i>Пожалуйста, будь вежлив — "
        "мы работаем для тебя с любовью ❤️</i>"
    )
    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="↩️ Назад",
                        callback_data="back"
                    )
                ]
            ]
        )
    )
    await callback.answer()

# ─── FAQ ──────────────────────────────────

@dp.callback_query(F.data == "faq")
async def faq(callback: CallbackQuery):
    text = (
        "❓ <b>Часто задаваемые вопросы</b>\n\n"
        "<b>— Это бесплатно?</b>\n"
        "Пока да! Мы в бета-тесте, "
        "так что всё абсолютно бесплатно. "
        "Тестируй, пробуй, рассказывай друзьям!\n\n"
        "<b>— Ключ не работает, что делать?</b>\n"
        "Попробуй другой протокол или "
        "напиши мне в поддержку. Иногда "
        "сервера устают и им нужен отдых.\n\n"
        "<b>— А вас не заблокируют?</b>\n"
        "Мы делаем всё возможное, чтобы "
        "сервис работал стабильно. Но всякое "
        "бывает — мы к этому готовы.\n\n"
        "<b>— Сколько серверов?</b>\n"
        "Пока немного, но мы растём! "
        "Следи за обновлениями."
    )

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="↩️ Назад",
                        callback_data="back"
                    )
                ]
            ]
        )
    )
    await callback.answer()

# ─── О проекте ────────────────────────────

@dp.callback_query(F.data == "about")
async def about(callback: CallbackQuery):
    text = (
        "💜 <b>О проекте LunaicsCatsVPN</b>\n\n"
        "Это не просто VPN-сервис. "
        "Это история о свободе, котиках "
        "и желании сделать интернет "
        "немного лучше.\n\n"
        "Меня создал один человек, "
        "который верит, что каждый "
        "заслуживает доступ к информации "
        "без ограничений.\n\n"
        "<b>Версия:</b> 0.1 Beta 🧪\n"
        "<b>Статус:</b> Активно развиваемся\n\n"
        "<i>Используйте сервис с умом "
        "и помните — любая технология "
        "должна служить добру.</i>\n\n"
        "🐱 Мяу!"
    )

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="↩️ Назад",
                        callback_data="back"
                    )
                ]
            ]
        )
    )
    await callback.answer()

# ─── Оплата ───────────────────────────────

@dp.callback_query(F.data == "payment")
async def payment(callback: CallbackQuery):
    text = (
        "━━━━━━━━━━━━━━━━━━\n"
        " 💳 <b>ОПЛАТА VPN</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "<b>Тариф:</b>\n"
        "• 1 месяц — <b>199₽</b>\n\n"
        "<b>Реквизиты СБП:</b>\n\n"
        "📱 Телефон:\n"
        "<code>+7 951 380 01 01</code>\n\n"
        "🏦 Банк:\n"
        "<b>Альфа‑Банк</b>\n\n"
        "💰 Сумма:\n"
        "<b>199₽</b>\n\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "<b>Как оплатить:</b>\n"
        "1. Откройте приложение банка\n"
        "2. Перевод по СБП\n"
        "3. Введите номер и сумму\n"
        "4. Выберите <b>Альфа‑Банк</b>\n"
        "5. Нажмите кнопку ниже\n"
        "   и приложите скриншот оплаты\n\n"
        "⚠️ Доступ активируется "
        "после подтверждения оплаты."
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Я оплатил",
                    callback_data="paid"
                )
            ],
            [
                InlineKeyboardButton(
                    text="↩️ Назад",
                    callback_data="back"
                )
            ]
        ]
    )

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(F.data == "paid")
async def process_payment(callback: CallbackQuery):
    text = (
        "📸 <b>Отлично!</b>\n\n"
        "Пожалуйста, отправь сюда скриншот "
        "или квитанцию об оплате (можно прямо "
        "из галереи, я пойму 😉).\n\n"
        "Я передам его администратору, "
        "и он активирует твой доступ вручную.\n\n"
        "<i>Скриншот нужен для проверки, "
        "чтобы всё было честно и быстро.</i>"
    )

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="↩️ Отмена",
                        callback_data="back"
                    )
                ]
            ]
        )
    )
    await callback.answer()

# ─── Приём скриншота оплаты ───────────────

@dp.message(F.content_type.in_([ContentType.PHOTO, ContentType.DOCUMENT]))
async def handle_payment_screenshot(message: Message):
    user = message.from_user
    username = user.username or "не указан"
    first_name = user.first_name or "Имя не указано"

    caption = (
        f"📩 <b>Новая оплата!</b>\n"
        f"👤 {first_name}\n"
        f"🆔 <code>{user.id}</code>\n"
        f"💬 @{username}\n\n"
        "Отправь этому пользователю ключ после проверки."
    )

    if message.photo:
        await bot.send_photo(
            ADMIN_ID,
            message.photo[-1].file_id,
            caption=caption
        )
    elif message.document:
        await bot.send_document(
            ADMIN_ID,
            message.document.file_id,
            caption=caption
        )
    else:
        return

    await message.answer(
        "✅ <b>Спасибо!</b>\n"
        "Я получил твой скриншот и отправил "
        "его на проверку.\n\n"
        "Обычно это занимает до 15 минут. "
        "Если долго нет ответа — постучись "
        "в поддержку (@sibpollerty).\n\n"
        "<i>Ты большой молодец, что с нами! 🐱</i>"
    )

# ─── Навигация ────────────────────────────

@dp.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    text = (
        "🏠 <b>Мы снова дома!</b>\n\n"
        "Выбирай, что хочешь сделать, "
        "и я с радостью помогу.\n\n"
        "<i>Не забывай — мы в бете, "
        "так что возможны сюрпризы!</i>"
    )

    await callback.message.edit_text(
        text,
        reply_markup=main_menu
    )
    await callback.answer("Возвращаемся...")

# ─── Админка ──────────────────────────────

@dp.message(Command("adsibsib"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🤫 Эта дверь не для тебя, друг.")
        return

    uptime = datetime.now() - start_time

    text = (
        "⚙️ <b>Привет, создатель!</b>\n\n"
        f"👥 С нами уже: <code>{len(users)}</code> человек\n"
        f"⏱ Не спим: <code>{str(uptime).split('.')[0]}</code>\n"
        "🟢 Всё работает\n\n"
        "<i>Ты молодец, продолжай в том же духе!</i>"
    )

    await message.answer(text, reply_markup=admin_menu)

@dp.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    uptime = datetime.now() - start_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    # Средний балл
    if ratings:
        all_scores = [v["score"] for v in ratings.values()]
        avg = sum(all_scores) / len(all_scores)
        rating_line = f"⭐️ Средний балл: <code>{avg:.1f}/5</code> ({len(all_scores)} оценок)\n"
    else:
        rating_line = "⭐️ Оценок пока нет\n"

    text = (
        "📊 <b>Статистика для своих</b>\n\n"
        f"👥 Пользователей: <code>{len(users)}</code>\n"
        f"⏱ Время работы: <code>{days}д {hours}ч {minutes}м</code>\n"
        f"{rating_line}"
        "🟢 Статус: Живой\n\n"
        "<i>Бета-тест продолжается. "
        "Люди приходят — это радует!</i>"
    )

    await callback.message.edit_text(text, reply_markup=admin_menu)
    await callback.answer()

@dp.callback_query(F.data == "admin_users")
async def admin_users(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    if not users:
        text = "😢 Пока никто не пришёл. Но это временно!"
    else:
        text = "👥 <b>Наши замечательные пользователи</b>\n\n"
        for uid, data in users.items():
            user_rating = ratings.get(uid)
            stars = (
                "⭐️" * user_rating["score"]
                if user_rating else "без оценки"
            )
            text += (
                f"🌟 {data['first_name']}\n"
                f"   ID: <code>{uid}</code>\n"
                f"   @{data.get('username', 'нет')}\n"
                f"   Оценка: {stars}\n\n"
            )

    await callback.message.edit_text(text, reply_markup=admin_menu)
    await callback.answer()

@dp.callback_query(F.data == "admin_ratings")
async def admin_ratings(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    if not ratings:
        text = "⭐️ Оценок пока нет. Жди, скоро придут!"
    else:
        all_scores = [v["score"] for v in ratings.values()]
        avg = sum(all_scores) / len(all_scores)

        # Распределение
        dist = {i: 0 for i in range(1, 6)}
        for v in ratings.values():
            dist[v["score"]] += 1

        emoji_map = {1: "😞", 2: "😕", 3: "😐", 4: "😊", 5: "🔥"}

        text = (
            f"⭐️ <b>Рейтинг бота</b>\n\n"
            f"Средний балл: <b>{avg:.1f}/5</b>\n"
            f"Всего оценок: <b>{len(all_scores)}</b>\n\n"
            "Распределение:\n"
        )
        for score in range(5, 0, -1):
            count = dist[score]
            bar = "█" * count if count else "—"
            text += f"{score} {emoji_map[score]} {bar} ({count})\n"

    await callback.message.edit_text(text, reply_markup=admin_menu)
    await callback.answer()

@dp.callback_query(F.data == "admin_send_survey")
async def admin_send_survey(callback: CallbackQuery):
    """Разослать запрос оценки всем пользователям."""
    if callback.from_user.id != ADMIN_ID:
        return

    sent = 0
    failed = 0

    for uid, data in users.items():
        try:
            await bot.send_message(
                uid,
                f"Привет, <b>{data['first_name']}</b>! 🐱\n\n"
                "Ты уже пользовался нашим ботом.\n"
                "Нам очень важно твоё мнение — "
                "это поможет сделать сервис лучше.\n\n"
                "Как тебе <b>LunaicsCatsVPN</b>?\n"
                "Оцени от 1 до 5, пожалуйста 🙏",
                reply_markup=rating_menu
            )
            sent += 1
            # Небольшая пауза чтобы не словить флуд
            await asyncio.sleep(0.1)
        except Exception:
            failed += 1

    await callback.message.edit_text(
        f"📢 <b>Рассылка завершена!</b>\n\n"
        f"✅ Отправлено: <code>{sent}</code>\n"
        f"❌ Не доставлено: <code>{failed}</code>\n\n"
        "<i>Жди оценок, они придут!</i>",
        reply_markup=admin_menu
    )
    await callback.answer()

@dp.callback_query(F.data == "close")
async def close(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer("Панель закрыта!")

# ─── Запуск ───────────────────────────────

async def main():
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
    from aiohttp import web

    RENDER = os.getenv("RENDER")

    if RENDER:
        WEBHOOK_HOST = os.getenv("RENDER_EXTERNAL_URL")
        WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
        WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

        app = web.Application()
        webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
        webhook_requests_handler.register(app, path=WEBHOOK_PATH)
        setup_application(app, dp, bot=bot)

        await bot.set_webhook(WEBHOOK_URL)
        print(f"🐱 Вебхук установлен: {WEBHOOK_URL}")

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
        await site.start()

        await asyncio.Event().wait()
    else:
        print("🐱 LunaicsCatsVPN запущен и мурлычет локально!")
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())