import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === Kalitlar ===
BOT_TOKEN = "8207707024:AAEzU8yMlI5vjw4bbZCE5FDfVkZU-t0fuxo"
HIVE_API_KEY = "1jBUPlpfGQTH8YIzVLTnfQ=="

# === Rasm generatsiya funksiyasi ===
def generate_image(prompt):
    url = "https://api.thehive.ai/api/v1/image/generate"
    headers = {"Authorization": f"Bearer {HIVE_API_KEY}"}
    data = {"model": "hive:stable-diffusion", "prompt": prompt}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        if "images" in result and len(result["images"]) > 0:
            return result["images"][0]["url"]
    return None

# === /start buyrug‘i ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Menga prompt yubor, men Hive yordamida rasm yarataman 🎨")

# === Prompt yuborilganda ===
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("Iltimos, rasm tavsifini yoz: /generate <prompt>")
        return

    await update.message.reply_text("⏳ Rasm yaratilmoqda, kuting...")

    img_url = generate_image(prompt)
    if img_url:
        await update.message.reply_photo(img_url, caption=f"✅ Tayyor rasm: {prompt}")
    else:
        await update.message.reply_text("❌ Xatolik yuz berdi yoki API javob bermadi.")

# === Botni ishga tushirish ===
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("generate", generate))

print("🤖 Bot ishlayapti...")
app.run_polling()
