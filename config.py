from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "0").split(",")))
DB_PATH = "lunaticcat.db"

VPN_SERVERS = {
    "🇺🇸 США 1": {
        "flag": "🇺🇸",
        "country": "США",
        "city": "New York",
        "ping": "~89ms",
        "load": "low",
        "key": "vmess://eyJ2IjoiMiIsInBzIjoiXHUyNmY4XHVmZTBmXHUyNmY4XHVmZTBmIiwiYWRkIjoic2VydmVyMy5iZWhsZXNodGJhbmVoLmNvbSIsInBvcnQiOiIyMDQwMSIsImlkIjoiNmEzYmNjMDgtOWM3Ny00YzAyLTg0NGItNGE2OTQzNGYyZmVhIiwiYWlkIjoiMCIsIm5ldCI6IndzIiwicGF0aCI6Ii8iLCJ0bHMiOiIifQ=="
    },
    "🇺🇸 США 2": {
        "flag": "🇺🇸",
        "country": "США",
        "city": "Los Angeles",
        "ping": "~95ms",
        "load": "medium",
        "key": "ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpkNjEwNWJiZC1iZTBkLTQ1YjItODJhZC0zMWZkMTA3MWMxZDI@service.ouluyu n9803.com:20003"
    },
    "🇨🇦 Канада": {
        "flag": "🇨🇦",
        "country": "Канада",
        "city": "Toronto",
        "ping": "~75ms",
        "load": "low",
        "key": "ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpkNjEwNWJiZC1iZTBkLTQ1YjItODJhZC0zMWZkMTA3MWMxZDI@service.ouluyu n9803.com:26667"
    },
    "🇯🇵 Япония": {
        "flag": "🇯🇵",
        "country": "Япония",
        "city": "Tokyo",
        "ping": "~145ms",
        "load": "low",
        "key": "vmess://eyJhZGQiOiJzZXJ2ZXIzMi5iZWhsZXNodGJhbmVoLmNvbSIsInBvcnQiOiI0NDMiLCJpZCI6IjRiYThiZWRkLTcyODUtNDcyYS1iYzE0LWZiOTFkYzZiZTRjOSIsImFpZCI6IjAiLCJuZXQiOiJ3cyIsInBhdGgiOiIvIiwidGxzIjoiIn0="
    },
    "🇩🇪 Германия": {
        "flag": "🇩🇪",
        "country": "Германия",
        "city": "Frankfurt",
        "ping": "~35ms",
        "load": "low",
        "key": "vmess://eyJhZGQiOiJzZXJ2ZXIzMS5iZWhsZXNodGJhbmVoLmNvbSIsInBvcnQiOiI0NDMiLCJpZCI6IjE4MjgzZDItZTk2OC00MmUxLTgwZDAtMTJmYTJmNWQzOGQ2IiwiYWlkIjoiMCIsIm5ldCI6IndzIiwicGF0aCI6Ii8iLCJ0bHMiOiIifQ=="
    }
}

FREE_KEYS_PER_DAY = 1
KEY_DURATION_DAYS = 1
CHANNEL_ID = "@VPNLunaticCat"