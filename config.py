from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "0").split(",")))
DB_PATH = "lunaticcat.db"

VPN_SERVERS = {
    "🇬🇧 Великобритания": {
        "flag": "🇬🇧",
        "country": "Великобритания",
        "city": "London",
        "ping": "~45ms",
        "load": "low",
        "key": "vless://08539045-5215-4757-b790-1e21e51c55cd@165.227.239.140:8443?encryption=none&security=reality&sni=zula.ir&fp=firefox&pbk=hMNiWJaGuUfAXwmb4pfsNpvXuCION6stZIV77IU-Eiw&sid=72fdacdd&spx=%2F&type=grpc#GB"
    },
    "🇸🇬 Сингапур 1": {
        "flag": "🇸🇬",
        "country": "Сингапур",
        "city": "Singapore",
        "ping": "~120ms",
        "load": "low",
        "key": "vless://fe1296e9-8a7f-4fbf-a669-f0c43f833e12@141.193.213.30:2083?encryption=none&security=tls&sni=fe1296e9-8a7f-4fbf-a669-f0c43f833e12.jonbandegan.online&type=ws&host=freak.jonbandegan.online&path=%2Fwss51157%3Fed%3D2048#SG1"
    },
    "🇸🇬 Сингапур 2": {
        "flag": "🇸🇬",
        "country": "Сингапур",
        "city": "Singapore",
        "ping": "~125ms",
        "load": "medium",
        "key": "vless://fe1296e9-8a7f-4fbf-a669-f0c43f833e12@mtn.ircf.space:2083?encryption=none&security=tls&sni=fe1296e9-8a7f-4fbf-a669-f0c43f833e12.jonbandegan.online&type=ws&host=freak.jonbandegan.online&path=%2Fwss51157%3Fed%3D2048#SG2"
    },
    "🇩🇪 Германия": {
        "flag": "🇩🇪",
        "country": "Германия",
        "city": "Frankfurt",
        "ping": "~35ms",
        "load": "low",
        "key": "vless://00000000-0000-4000-8000-000000000000@45.145.42.170:8005?allowInsecure=1&sni=sub.mot.ip-ddns.com&type=ws&host=sub.mot.ip-ddns.com&path=/security=tls#DE"
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