import discord
import requests
import os

TOKEN = "MTQ2MTM3NzMyMTQxMDc2MDczNg.GDvZ0a.tnqC5JjkEAcnKnxvTgiHOXQquz8ZAgnx0Pwa5M"
DEEPL_KEY = "961731b5-5df8-46d0-b173-66c69b9a6b7c:fx"
WEBHOOK_URL = "https://discord.com/api/webhooks/1461375983604207619/tGiwEXrqhlLfVu2-yM-TXbYUzvLORUR4RkoRykSnn9R_qEz6x4-N5tyYPTefkbFcB_c5"

JP_ROLE = "JP"
KR_ROLE = "KR"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)


def deepl_translate(text, target):
    url = "https://api-free.deepl.com/v2/translate"
    data = {
        "auth_key": DEEPL_KEY,
        "text": text,
        "target_lang": target
    }
    res = requests.post(url, data=data)
    return res.json()["translations"][0]["text"]


def send_webhook(name, avatar, msg):
    data = {
        "username": name,
        "avatar_url": avatar,
        "content": msg
    }
    requests.post(WEBHOOK_URL, json=data)


@client.event
async def on_message(message):
    if message.author.bot:
        return

    roles = [r.name for r in message.author.roles]

    # 🇯🇵 → 🇰🇷
    if JP_ROLE in roles:
        translated = deepl_translate(message.content, "KO")
        final_msg = f"🇯🇵 → 🇰🇷 {translated}"

        send_webhook(
            message.author.display_name,
            message.author.avatar.url,
            final_msg
        )

    # 🇰🇷 → 🇯🇵
    if KR_ROLE in roles:
        translated = deepl_translate(message.content, "JA")
        final_msg = f"🇰🇷 → 🇯🇵 {translated}"

        send_webhook(
            message.author.display_name,
            message.author.avatar.url,
            final_msg
        )


client.run(TOKEN)