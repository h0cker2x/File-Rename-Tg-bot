import telebot
from telebot import types
import os
import io
import logging
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file (local development)
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN environment variable not set!")
    raise ValueError("BOT_TOKEN environment variable not set!")

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# Developer info
DEV_USERNAME = "@ghty_verma5"
CHANNEL_USERNAME = "@dewanshworld0"

# Store user data
user_files = {}

# Emojis
EMOJI = {
    'welcome': '🌟',
    'file': '📁',
    'success': '✅',
    'error': '❌',
    'wait': '⏳',
    'rename': '✏️',
    'done': '🎉',
    'info': 'ℹ️',
    'arrow': '➡️',
    'star': '⭐',
    'fire': '🔥',
    'crown': '👑',
    'heart': '❤️',
    'rocket': '🚀'
}

@bot.message_handler(commands=['start'])
def start_command(message):
    """Welcome message with best UI"""
    user = message.from_user
    user_id = user.id
    first_name = user.first_name
    username = f"@{user.username}" if user.username else "No username"
    
    welcome_text = (
        f"{EMOJI['welcome']}━━━━━━━━━━━━━━━━━━━{EMOJI['welcome']}\n"
        f"     𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐁𝐎𝐓     \n"
        f"{EMOJI['welcome']}━━━━━━━━━━━━━━━━━━━{EMOJI['welcome']}\n\n"
        
        f"{EMOJI['heart']} **Hello {first_name}!**\n"
        f"{EMOJI['info']} **User ID:** `{user_id}`\n"
        f"{EMOJI['file']} **Username:** {username}\n\n"
        
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"{EMOJI['rocket']} **FILE RENAME BOT** {EMOJI['rocket']}\n"
        f"━━━━━━━━━━━━━━━━━━━\n\n"
        
        f"{EMOJI['star']} **Features:**\n"
        f"├─ {EMOJI['file']} File Upload\n"
        f"├─ {EMOJI['rename']} Custom Rename\n"
        f"├─ {EMOJI['success']} Auto Extension\n"
        f"├─ {EMOJI['info']} File Info\n"
        f"└─ {EMOJI['rocket']} Fast Processing\n\n"
        
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📋 **How to Use:**\n"
        f"━━━━━━━━━━━━━━━━━━━\n\n"
        
        f"1️⃣ **Send** any file {EMOJI['file']}\n"
        f"2️⃣ **Enter** new name {EMOJI['rename']}\n"
        f"3️⃣ **Get** renamed file {EMOJI['success']}\n\n"
        
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ **Commands:**\n"
        f"━━━━━━━━━━━━━━━━━━━\n\n"
        
        f"{EMOJI['arrow']} /start - Welcome\n"
        f"{EMOJI['arrow']} /help - Help Guide\n"
        f"{EMOJI['arrow']} /cancel - Cancel\n"
        f"{EMOJI['arrow']} /status - Bot Status\n\n"
        
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"{EMOJI['heart']} **Join Channel** {EMOJI['heart']}\n"
        f"━━━━━━━━━━━━━━━━━━━\n\n"
        
        f"📢 {CHANNEL_USERNAME}\n"
        f"👨‍💻 Dev: {DEV_USERNAME}\n\n"
        
        f"{EMOJI['crown']}━━━━━━━━━━━━━━━━━━━{EMOJI['crown']}\n"
        f"⚡ **Ready to rename!** ⚡\n"
        f"{EMOJI['crown']}━━━━━━━━━━━━━━━━━━━{EMOJI['crown']}"
    )
    
    # Create inline buttons
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton(f"{EMOJI['file']} Send File", callback_data="send_file")
    btn2 = types.InlineKeyboardButton("❓ Help", callback_data="help")
    btn3 = types.InlineKeyboardButton(f"{EMOJI['heart']} Channel", url=f"https://t.me/dewanshworld0")
    btn4 = types.InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/ghty_verma5")
    btn5 = types.InlineKeyboardButton("📊 Status", callback_data="status")
    btn6 = types.InlineKeyboardButton(f"{EMOJI['star']} Rate", url="https://t.me/dewanshworld0")
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    
    bot.send_message(user_id, welcome_text, reply_markup=markup, parse_mode='Markdown')
    logger.info(f"User {user_id} started bot")
    logger.info(f"Bot token loaded: {BOT_TOKEN[:10]}...")

@bot.message_handler(commands=['help'])
def help_command(message):
    """Help guide"""
    help_text = (
        "❓ **HELP GUIDE**\n\n"
        f"{EMOJI['rocket']} **How to rename files:**\n"
        f"1️⃣ Send a file (as document)\n"
        f"2️⃣ Type the new name\n"
        f"3️⃣ Get renamed file\n\n"
        
        f"{EMOJI['file']} **Supported files:**\n"
        f"• Documents (pdf, doc, txt)\n"
        f"• Archives (zip, rar, 7z)\n"
        f"• Apps (apk, ipa, exe)\n"
        f"• Media (mp3, mp4, jpg, png)\n"
        f"• And any other file type!\n\n"
        
        f"{EMOJI['info']} **Commands:**\n"
        f"/start - Main menu\n"
        f"/help - This guide\n"
        f"/cancel - Cancel process\n"
        f"/status - Check bot status\n\n"
        
        f"{EMOJI['heart']} **Channel:** {CHANNEL_USERNAME}\n"
        f"👨‍💻 **Dev:** {DEV_USERNAME}"
    )
    
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(f"{EMOJI['heart']} Join Channel", url=f"https://t.me/dewanshworld0")
    markup.add(btn)
    
    bot.reply_to(message, help_text, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def status_command(message):
    """Bot status"""
    user_id = message.from_user.id
    uptime = time.time() - start_time
    
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    seconds = int(uptime % 60)
    
    status_text = (
        f"📊 **BOT STATUS**\n\n"
        f"{EMOJI['success']} **Status:** Online\n"
        f"⏱️ **Uptime:** {hours}h {minutes}m {seconds}s\n"
        f"👥 **Active Users:** {len(user_files)}\n"
        f"📁 **Files Processed:** Working\n\n"
        f"{EMOJI['heart']} **Channel:** {CHANNEL_USERNAME}\n"
        f"👨‍💻 **Developer:** {DEV_USERNAME}"
    )
    
    bot.reply_to(message, status_text, parse_mode='Markdown')

@bot.message_handler(commands=['cancel'])
def cancel_command(message):
    """Cancel current operation"""
    user_id = message.from_user.id
    
    if user_id in user_files:
        del user_files[user_id]
        bot.reply_to(message, f"{EMOJI['success']} Operation cancelled! Send /start to begin again.")
        logger.info(f"User {user_id} cancelled operation")
    else:
        bot.reply_to(message, f"{EMOJI['info']} No active operation to cancel.")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    """Handle incoming files"""
    user_id = message.from_user.id
    
    try:
        # Get file info
        file_info = message.document
        file_name = file_info.file_name
        file_size = file_info.file_size
        file_id = file_info.file_id
        mime_type = file_info.mime_type
        
        # Get file extension
        file_ext = os.path.splitext(file_name)[1]
        
        # Format file size
        if file_size < 1024:
            size_text = f"{file_size} B"
        elif file_size < 1024 * 1024:
            size_text = f"{file_size / 1024:.1f} KB"
        else:
            size_text = f"{file_size / (1024 * 1024):.1f} MB"
        
        # Store file data
        user_files[user_id] = {
            'file_id': file_id,
            'file_name': file_name,
            'file_ext': file_ext,
            'file_size': file_size,
            'mime_type': mime_type,
            'timestamp': time.time()
        }
        
        # Send file info
        info_text = (
            f"{EMOJI['success']} **File Received!**\n\n"
            f"{EMOJI['file']} **Name:** `{file_name}`\n"
            f"📦 **Size:** {size_text}\n"
            f"🔖 **Extension:** `{file_ext}`\n"
            f"📋 **Type:** `{mime_type}`\n\n"
            f"{EMOJI['rename']} **Now send me the new name** (without extension):"
        )
        
        bot.reply_to(message, info_text, parse_mode='Markdown')
        logger.info(f"User {user_id} uploaded: {file_name} ({size_text})")
        
    except Exception as e:
        logger.error(f"Error handling file: {e}")
        bot.reply_to(message, f"{EMOJI['error']} Error: {str(e)[:50]}")

@bot.message_handler(func=lambda message: message.from_user.id in user_files)
def handle_new_name(message):
    """Handle new filename"""
    user_id = message.from_user.id
    
    try:
        # Get new name
        new_name = message.text.strip()
        
        if not new_name:
            bot.reply_to(message, f"{EMOJI['error']} Name cannot be empty! Please try again:")
            return
        
        # Validate filename
        if len(new_name) > 100:
            bot.reply_to(message, f"{EMOJI['error']} Name too long! Max 100 characters. Try again:")
            return
        
        # Remove invalid characters
        valid_chars = "".join(c for c in new_name if c.isalnum() or c in (' ', '-', '_', '.'))
        valid_chars = valid_chars.strip()
        
        if not valid_chars:
            bot.reply_to(
                message, 
                f"{EMOJI['error']} Invalid characters! Use letters, numbers, spaces, - _ . only.\nTry again:"
            )
            return
        
        # Get file data
        file_data = user_files.get(user_id)
        if not file_data:
            bot.reply_to(message, f"{EMOJI['error']} Session expired! Send file again.")
            del user_files[user_id]
            return
        
        # Create new filename
        original_name = file_data['file_name']
        file_ext = file_data['file_ext']
        new_filename = f"{valid_chars}{file_ext}"
        
        # Send processing message
        status_msg = bot.reply_to(
            message,
            f"{EMOJI['wait']} Processing...\n\n"
            f"Original: `{original_name}`\n"
            f"New: `{new_filename}`",
            parse_mode='Markdown'
        )
        
        # Download file
        file_id = file_data['file_id']
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Update status
        bot.edit_message_text(
            f"{EMOJI['wait']} Uploading renamed file...",
            user_id,
            status_msg.message_id
        )
        
        # Send renamed file
        bot.send_document(
            user_id,
            downloaded_file,
            visible_file_name=new_filename,
            caption=f"{EMOJI['done']} **Rename Complete!**\n\n"
                   f"📝 Original: `{original_name}`\n"
                   f"📄 New: `{new_filename}`",
            parse_mode='Markdown'
        )
        
        # Delete status message
        bot.delete_message(user_id, status_msg.message_id)
        
        # Clear user data
        del user_files[user_id]
        
        # Ask for next action
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton(f"{EMOJI['file']} Rename Another", callback_data="rename_another")
        btn2 = types.InlineKeyboardButton("❌ Cancel", callback_data="cancel_action")
        markup.add(btn1, btn2)
        
        bot.send_message(
            user_id,
            f"{EMOJI['done']} **What would you like to do?**",
            parse_mode='Markdown',
            reply_markup=markup
        )
        
        logger.info(f"User {user_id} renamed: {original_name} → {new_filename}")
        
    except Exception as e:
        logger.error(f"Error renaming: {e}")
        bot.reply_to(message, f"{EMOJI['error']} Error: {str(e)[:100]}")
        if user_id in user_files:
            del user_files[user_id]

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    """Handle button callbacks"""
    user_id = call.message.chat.id
    
    try:
        if call.data == "send_file":
            bot.edit_message_text(
                f"{EMOJI['file']} **Send me any file!**\n\n"
                f"I'll ask for new name after receiving.",
                user_id,
                call.message.message_id,
                parse_mode='Markdown'
            )
            
        elif call.data == "help":
            help_text = (
                "❓ **HELP GUIDE**\n\n"
                f"{EMOJI['rocket']} **Steps:**\n"
                f"1️⃣ Send a file\n"
                f"2️⃣ Type new name\n"
                f"3️⃣ Get renamed file\n\n"
                f"{EMOJI['file']} **Any file works!**"
            )
            bot.edit_message_text(
                help_text,
                user_id,
                call.message.message_id,
                parse_mode='Markdown'
            )
            
        elif call.data == "status":
            status_text = (
                f"📊 **SYSTEM STATUS**\n\n"
                f"{EMOJI['success']} Bot: Online\n"
                f"👥 Active: {len(user_files)}\n"
                f"{EMOJI['heart']} Channel: Active"
            )
            bot.edit_message_text(
                status_text,
                user_id,
                call.message.message_id,
                parse_mode='Markdown'
            )
            
        elif call.data == "rename_another":
            bot.edit_message_text(
                f"{EMOJI['file']} **Send me a file to rename!**",
                user_id,
                call.message.message_id,
                parse_mode='Markdown'
            )
            
        elif call.data == "cancel_action":
            if user_id in user_files:
                del user_files[user_id]
            bot.edit_message_text(
                f"{EMOJI['success']} **Cancelled!**\n\nSend /start to begin again.",
                user_id,
                call.message.message_id,
                parse_mode='Markdown'
            )
        
        bot.answer_callback_query(call.id)
        
    except Exception as e:
        logger.error(f"Callback error: {e}")

@bot.message_handler(content_types=['photo', 'audio', 'video', 'voice'])
def handle_other_media(message):
    """Handle non-document files"""
    bot.reply_to(
        message,
        f"{EMOJI['info']} Please send files as **documents**.\n\n"
        f"Click on 📎 → 📁 Document → Select file"
    )

@bot.message_handler(func=lambda message: True)
def handle_other(message):
    """Handle other messages"""
    user_id = message.from_user.id
    
    if user_id in user_files:
        bot.reply_to(
            message,
            f"{EMOJI['rename']} Please send the new name for your file:"
        )
    else:
        bot.reply_to(
            message,
            f"{EMOJI['info']} Send /start to begin.\nOr send a file to rename!"
        )

# Cleanup old data function
def cleanup_old_data():
    """Remove old user data"""
    while True:
        try:
            current_time = time.time()
            for user_id in list(user_files.keys()):
                if current_time - user_files[user_id].get('timestamp', 0) > 300:  # 5 minutes
                    del user_files[user_id]
                    logger.info(f"Cleaned user {user_id}")
            time.sleep(60)
        except:
            pass

# Start cleanup thread
import threading
cleanup_thread = threading.Thread(target=cleanup_old_data, daemon=True)
cleanup_thread.start()

# Record start time
start_time = time.time()

# Main bot loop
if __name__ == '__main__':
    print(f"{EMOJI['rocket']} Bot started...")
    print(f"{EMOJI['heart']} Developer: {DEV_USERNAME}")
    print(f"{EMOJI['file']} Channel: {CHANNEL_USERNAME}")
    print(f"{EMOJI['success']} Bot token loaded from environment variable")
    print("-" * 30)
    
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=30)
        except Exception as e:
            print(f"Error: {e}")
            print("Restarting in 5 seconds...")
            time.sleep(5)
