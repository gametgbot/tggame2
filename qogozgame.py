from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
import random

# Inline tugmalar bilan foydalanuvchiga belgi tanlash
async def send_random_symbol(update: Update, context: CallbackContext):
    # Inline tugmalarni yaratish
    keyboard = [
        [
            InlineKeyboardButton("✊", callback_data='✊'),
            InlineKeyboardButton("🤚", callback_data='🤚'),
            InlineKeyboardButton("✌️", callback_data='✌️')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Iltimos, biror bir belgini tanlang:', reply_markup=reply_markup)

# Foydalanuvchi o'z belgisini yuborganida ishlaydigan funksiya
async def receive_user_choice(update: Update, context: CallbackContext):
    user_choice = update.message.text.strip()
    if user_choice not in ['✊', '🤚', '✌️']:
        await update.message.reply_text("Iltimos, faqat ✊, 🤚 yoki ✌️ ni yuboring!")
        return

    # Bot tasodifiy belgi tanlaydi
    symbols = ['✊', '🤚', '✌️']
    random_symbol = random.choice(symbols)

    # Durrang yoki g'olibni aniqlash
    result_text = f'Siz tanlagan belgi: {user_choice}\nBotning tasodifiy belgisi: {random_symbol}\n'

    # O'yin natijasi
    if user_choice == random_symbol:
        result_text += "O'yin durrang!\n"
    elif (user_choice == '✊' and random_symbol == '🤚') or \
         (user_choice == '🤚' and random_symbol == '✌️') or \
         (user_choice == '✌️' and random_symbol == '✊'):
        result_text += "Siz g\'olibsiz!\n"
    else:
        result_text += "Bot g\'olib!\n"

    await update.message.reply_text(result_text)

# Botni ishga tushurish
def main():
    token = '7827493041:AAGyoXIgBuA3XvY3s1fIxoZLolRuaUO8Do0'  # Sizning tokeningiz
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", send_random_symbol))  # /start komandasini qo'shish
    application.add_handler(CallbackQueryHandler(receive_user_choice))  # Inline tugmalarni qayta ishlash
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_user_choice))  # Foydalanuvchi yuborgan matnni qabul qilish

    application.run_polling()  # Bu yerda asyncio.run()ni olib tashladik

if __name__ == '__main__':
    main()