from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "0").split(",")))
DB_PATH = "lunaticcat.db"

VPN_SERVERS = {
    "🇨🇦 Канада": {
        "flag": "🇨🇦",
        "country": "Канада",
        "city": "Canada",
        "ping": "~80ms",
        "load": "low",
        "key": "ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpBUmd2R1p5d0ErZ2FjZ0dWMjZCdm11MDUrd1ptUlcvaitBZFUrWjhCdDQ0PQ==@79.127.200.169:990#CA"
    },
    "🇺🇸 США 1": {
        "flag": "🇺🇸",
        "country": "США",
        "city": "New York",
        "ping": "~89ms",
        "load": "medium",
        "key": "ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M=@156.146.38.170:443#US1"
    },
    "🇺🇸 США 2": {
        "flag": "🇺🇸",
        "country": "США",
        "city": "Los Angeles",
        "ping": "~95ms",
        "load": "low",
        "key": "ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M=@156.146.38.167:443#US2"
    },
    "🇺🇸 США 3": {
        "flag": "🇺🇸",
        "country": "США",
        "city": "Chicago",
        "ping": "~92ms",
        "load": "medium",
        "key": "ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M=@37.19.198.236:443#US3"
    },
    "🇺🇸 США 4": {
        "flag": "🇺🇸",
        "country": "США",
        "city": "Dallas",
        "ping": "~98ms",
        "load": "high",
        "key": "ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M=@37.19.198.236:443#US4"
    }
}

FREE_KEYS_PER_DAY = 1
KEY_DURATION_DAYS = 1
CHANNEL_ID = "@LunaticCatVPN"