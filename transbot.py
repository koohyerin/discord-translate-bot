import discord
from discord.ext import commands
import requests
import os
import re

# -------------------
# 환경변수
# -------------------
TOKEN = os.getenv("TOKEN")
DEEPL_KEY = os.getenv("DEEPL_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# -------------------
# 봇 설정
# -------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -------------------
# 봇 켜질 때
# -------------------
@bot.event
async def on_ready():
    print("✅ 번역봇 온라인")

# -------------------
# 웃음 / 이모지 필터
# -------------------
def is_only_laugh_or_emoji(text):
    # 특수문자, 이모지 제거
    text = re.sub(r'[^\w\sㄱ-ㅎ가-힣]', '', text)
    text = text.strip()

    laugh_patterns = ["ㅋㅋ", "ㅎㅎ", "ㅠㅠ", "ㅜㅜ"]

    for p in laugh_patterns:
        if text.replace(p, "") == "":
            return True

    # 글자 자체가 없으면 (이모지만 보낸 경우)
    if text == "":
        return True

    return False

# -------------------
# DeepL 번역
# -------------------
def deepl_translate(text, target):
    url = "https://api-free.deepl.com/v2/translate"

    data = {
        "auth_key": DEEPL_KEY,
        "text": text,
        "target_lang": target
    }

    res = requests.post(url, data=data)
    return res.json()["translations"][0]["text"]

# -------------------
# 웹후크 전송
# -------------------
def send_webhook(name, avatar, msg):
    payload = {
        "username": name,
        "avatar_url": avatar,
        "content": msg
    }

    requests.post(WEBHOOK_URL, json=payload)

# -------------------
# 메시지 감지
# -------------------
@bot.event
async def on_message(message):

    # 봇 메시지 무시
    if message.author.bot:
        return

    # 웃음/이모지만 있으면 무시
    if is_only_laugh_or_emoji(message.content):
        return

    roles = [r.name for r in message.author.roles]

    # 🇯🇵 → 🇰🇷
    if "JP" in roles:
        translated = deepl_translate(message.content, "KO")
        final_msg = f"🇯🇵 → 🇰🇷 {translated}"

        send_webhook(
            message.author.display_name,
            message.author.avatar.url if message.author.avatar else None,
            final_msg
        )

    # 🇰🇷 → 🇯🇵
    elif "KR" in roles:
        translated = deepl_translate(message.content, "JA")
        final_msg = f"🇰🇷 → 🇯🇵 {translated}"

        send_webhook(
            message.author.display_name,
            message.author.avatar.url if message.author.avatar else None,
            final_msg
        )

# -------------------
# 실행
# -------------------
bot.run(TOKEN)