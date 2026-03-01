import telebot
from telebot import types
import os
import logging
import time
from dotenv import load_dotenv

load_dotenv()

# Bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

bot = telebot.TeleBot(BOT_TOKEN)

# Developer info
DEV_USERNAME = "@ghty_verma5"
CHANNEL_USERNAME = "@dewanshworld0"

# Store user data
user_files = {}

# Remove webhook on start
try:
    bot.remove_webhook()
    print("✅ Webhook removed")
except:
    print("⚠️ No webhook to remove")

@bot.message_handler(commands=['start'])
def start_command(message):
    user = message.from_user
    user_id = user.id
    first_name = user.first_name
    
    # Simple welcome text - NO MARKDOWN
    welcome_text = (
        "🌟━━━━━━━━━━━━━━━━━━━🌟\n"
        "     WELCOME TO BOT     \n"
        "🌟━━━━━━━━━━━━━━━━━━━🌟\n\n"
        
        f"👋 Hello {first_name}!\n"
        f"🆔 User ID: {user_id}\n\n"
        
        "━━━━━━━━━━━━━━━━━━━\n"
        "📁 FILE RENAME BOT\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        
        "📋 How to Use:\n"
        "1️⃣ Send any file\n"
        "2️⃣ Enter new name\n"
        "3️⃣ Get renamed file\n\n"
        
        "━━━━━━━━━━━━━━━━━━━\n"
        f"📢 {CHANNEL_USERNAME}\n"
        f"👨‍💻 {DEV_USERNAME}\n"
        "━━━━━━━━━━━━━━━━━━━"
    )
    
    # Buttons
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("📁 Send File", callback_data="send_file")
    btn2 = types.InlineKeyboardButton("❓ Help", callback_data="help")
    btn3 = types.InlineKeyboardButton("📢 Channel", url=f"https://t.me/dewanshworld0")
    btn4 = types.InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/ghty_verma5")
    markup.add(btn1, btn2, btn3, btn4)
    
    # Send without parse_mode
    bot.send_message(user_id, welcome_text, reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "❓ HELP GUIDE\n\n"
        "How to rename files:\n"
        "1️⃣ Send a file\n"
        "2️⃣ Type new name\n"
        "3️⃣ Get renamed file\n\n"
        "Any file type supported!"
    )
    bot.reply_to(message, help_text)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    user_id = message.from_user.id
    
    try:
        file_info = message.document
        file_name = file_info.file_name
        file_id = file_info.file_id
        file_ext = os.path.splitext(file_name)[1]
        
        # Store file data
        user_files[user_id] = {
            'file_id': file_id,
            'file_name': file_name,
            'file_ext': file_ext,
            'timestamp': time.time()
        }
        
        bot.reply_to(
            message,
            f"✅ File received: {file_name}\n\n"
            f"✏️ Now send me the new name (without extension):"
        )
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

@bot.message_handler(func=lambda message: message.from_user.id in user_files)
def handle_new_name(message):
    user_id = message.from_user.id
    
    try:
        new_name = message.text.strip()
        
        if not new_name:
            bot.reply_to(message, "❌ Name cannot be empty! Try again:")
            return
        
        # Clean filename
        valid_chars = "".join(c for c in new_name if c.isalnum() or c in (' ', '-', '_'))
        
        if not valid_chars:
            bot.reply_to(message, "❌ Invalid characters! Try again:")
            return
        
        file_data = user_files[user_id]
        original_name = file_data['file_name']
        file_ext = file_data['file_ext']
        new_filename = f"{valid_chars}{file_ext}"
        
        # Download and send file
        file_info = bot.get_file(file_data['file_id'])
        downloaded_file = bot.download_file(file_info.file_path)
        
        bot.send_document(
            user_id,
            downloaded_file,
            visible_file_name=new_filename,
            caption=f"✅ Rename complete!\n\nOriginal: {original_name}\nNew: {new_filename}"
        )
        
        del user_files[user_id]
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")
        if user_id in user_files:
            del user_files[user_id]

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    if call.data == "send_file":
        bot.edit_message_text(
            "📁 Send me any file!",
            call.message.chat.id,
            call.message.message_id
        )
    elif call.data == "help":
        bot.edit_message_text(
            "❓ Send a file, then type new name!",
            call.message.chat.id,
            call.message.message_id
        )
    bot.answer_callback_query(call.id)

# Cleanup old data
def cleanup():
    while True:
        try:
            current_time = time.time()
            for uid in list(user_files.keys()):
                if current_time - user_files[uid].get('timestamp', 0) > 300:
                    del user_files[uid]
            time.sleep(60)
        except:
            pass

import threading
threading.Thread(target=cleanup, daemon=True).start()

# Start bot
if __name__ == '__main__':
    print("🚀 Bot started...")
    print(f"👨‍💻 Developer: {DEV_USERNAME}")
    print(f"📢 Channel: {CHANNEL_USERNAME}")
    print("-" * 30)
    
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=30, skip_pending=True)
        except Exception as e:
            print(f"Error: {e}")
            if "409" in str(e):
                print("⚠️ Bot already running! Stopping other instances...")
                time.sleep(10)
            else:
                print("Restarting in 5 seconds...")
                time.sleep(5)
