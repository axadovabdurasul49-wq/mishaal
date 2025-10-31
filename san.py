import telebot
import requests

BOT_TOKEN = "8207707024:AAEzU8yMlI5vjw4bbZCE5FDfVkZU-t0fuxo"
DEEP_API_KEY = "sk_0d665a75ac36a5ea9392f17b76e8b9c7fcdbb769d2cb0622b460563b4ff0c9d0"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "Salom! men misha rasm ratish va logo xizmatida yordam bera olaman ")

@bot.message_handler(func=lambda m: True)
def generate_image(msg):
    prompt = msg.text
    bot.reply_to(msg, "⏳ Rasm yaratilmoqda...")

    url = "https://api.deepai.org/api/v1/images/generate"
    headers = {"Authorization": f"Token {DEEP_API_KEY}"}
    data = {"prompt": prompt}

    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 200:
        img_url = res.json().get("data", [])[0].get("url")
        bot.send_photo(msg.chat.id, img_url)
    else:
        bot.reply_to(msg, "😢 Xatolik bo‘ldi, keyinroq urinib ko‘r!")

bot.polling()
