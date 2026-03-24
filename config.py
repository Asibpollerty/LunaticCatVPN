from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "0").split(",")))
DB_PATH = "lunaticcat.db"

VPN_SERVERS = {
    "🇩🇪 Германия": {
        "flag": "🇩🇪",
        "country": "Германия",
        "city": "Frankfurt",
        "ping": "~35ms",
        "load": "low",
        "key": "vless://00000000-0000-4000-8000-000000000000@45.145.42.170:8005?allowInsecure=1&sni=sub.mot.ip-ddns.com&type=ws&host=sub.mot.ip-ddns.com&path=/security=tls#DE"
    },
    "🇬🇧 Великобритания": {
        "flag": "🇬🇧",
        "country": "Великобритания",
        "city": "London",
        "ping": "~45ms",
        "load": "low",
        "key": "vless://48b36b6a-eaa6-4843-9231-0bb8b38b5da5@152.67.158.177:2443?allowInsecure=0&sni=www.cloudflare.com&flow=xtls-rprx-vision-udp443&fp=firefox&security=tls#GB"
    },
    "🇵🇱 Польша": {
        "flag": "🇵🇱",
        "country": "Польша",
        "city": "Warsaw",
        "ping": "~40ms",
        "load": "low",
        "key": "trojan://IL37892054@outgoing-ladybird.rooster465.autos:443?allowInsecure=0&sni=outgoing-ladybird.rooster465.autos#PL"
    },
    "🇷🇺 Россия": {
        "flag": "🇷🇺",
        "country": "Россия",
        "city": "Moscow",
        "ping": "~20ms",
        "load": "low",
        "key": "vless://9e4f36da-8f61-44f8-a9a7-0fd3a8d81234@193.9.49.65:443?allowInsecure=0&sni=r.icy.de5.net&type=ws&host=r.icy.de5.net&path=/?ed=2560security=tls#RU"
    },
    "🇺🇸 США": {
        "flag": "🇺🇸",
        "country": "США",
        "city": "New York",
        "ping": "~89ms",
        "load": "medium",
        "key": "vless://9e4f36da-8f61-44f8-a9a7-0fd3a8d81234@172.64.229.85:443?allowInsecure=0&sni=r.icy.de5.net&type=ws&host=r.icy.de5.net&path=/?ed=2560security=tls#US"
    }
}

FREE_KEYS_PER_DAY = 1
KEY_DURATION_DAYS = 1
CHANNEL_ID = "@VPNLunaticCat"