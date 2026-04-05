import os
import urllib.request
import urllib.parse
import time

# Список стран и их кодов из index.html
countries = {
    "eg": "🇪🇬",
    "mv": "🇲🇻",
    "tr": "🇹🇷",
    "vn": "🇻🇳",
    "cn": "🇨🇳",
    "mu": "🇲🇺",
    "th": "🇹🇭",
    "sc": "🇸🇨",
    "id": "🇮🇩",
    "lk": "🇱🇰",
    "tz": "🇹🇿",
    "tn": "🇹🇳"
}

# Директория для флагов
flags_dir = r"c:\Users\User\Downloads\tilda dododo\images\flags"
os.makedirs(flags_dir, exist_ok=True)

print(f"Начинаю скачивание флагов в {flags_dir}...")

# Тот же сервис, но через встроенную библиотеку urllib
headers = {'User-Agent': 'Mozilla/5.0'}

for code, emoji in countries.items():
    # Кодируем эмодзи для URL
    encoded_emoji = urllib.parse.quote(emoji)
    url = f"https://emojicdn.elk.sh/{encoded_emoji}"
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                filename = f"{code}.png"
                filepath = os.path.join(flags_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(response.read())
                print(f"✅ Флаг {code} ({emoji}) скачан")
            else:
                print(f"❌ Ошибка скачивания {code}: статус {response.status}")
        
        # Небольшая пауза, чтобы не нагружать сервис
        time.sleep(0.5)
        
    except Exception as e:
        print(f"❌ Ошибка при скачивании {code}: {str(e)}")

print("\nГотово! Все флаги успешно скачаны в папку images/flags/")
