import telebot
from telebot import types
import os
import io
import logging
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
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
    raise ValueError("❌ BOT_TOKEN not found in environment variables!")

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# Channel username (apna channel username daalein)
CHANNEL_USERNAME = '@YOUR_CHANNEL_USERNAME'  # Change this!

# Store user data
user_states = {}
user_files = {}

# Emojis
EMOJI = {
    'thumbs_up': '👍',
    'file': '📄',
    'success': '✅',
    'error': '❌',
    'wait': '⏳',
    'rename': '✏️',
    'done': '🎉',
    'info': 'ℹ️'
}

# Check if user is in channel
def is_user_in_channel(user_id):
    """Check if user has joined the required channel"""
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logger.error(f"Channel check error for user {user_id}: {e}")
        return False

@bot.message_handler(commands=['start'])
def start_command(message):
    """Handle /start command"""
    user_id = message.from_user.id
    username = message.from_user.first_name
    
    logger.info(f"User {user_id} (@{username}) started bot")
    
    if is_user_in_channel(user_id):
        welcome_text = (
            f"👋 **Welcome {username}!**\n\n"
            f"{EMOJI['file']} **File Rename Bot**\n\n"
            f"**How to use:**\n"
            f"1️⃣ Send me any file\n"
            f"2️⃣ Enter new name (without extension)\n"
            f"3️⃣ Get renamed file back\n\n"
            f"**Commands:**\n"
            f"/start - Show this message\n"
            f"/cancel - Cancel current operation\n"
            f"/status - Check bot status\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"Made with ❤️ by @YOUR_USERNAME"
        )
        bot.reply_to(message, welcome_text, parse_mode='Markdown')
    else:
        bot.reply_to(
            message,
            f"{EMOJI['error']} **Please join our channel first!**\n\n"
            f"📢 Channel: {CHANNEL_USERNAME}\n\n"
            f"Join karo phir /start karo.",
            parse_mode='Markdown'
        )

@bot.message_handler(commands=['cancel'])
def cancel_command(message):
    """Cancel current operation"""
    user_id = message.from_user.id
    
    if user_id in user_states:
        del user_states[user_id]
    if user_id in user_files:
        del user_files[user_id]
    
    bot.reply_to(
        message,
        f"{EMOJI['success']} Operation cancelled!\n\n"
        f"Send /start to begin again."
    )
    logger.info(f"User {user_id} cancelled operation")

@bot.message_handler(commands=['status'])
def status_command(message):
    """Check bot status"""
    user_id = message.from_user.id
    uptime = time.time() - start_time
    
    status_text = (
        f"{EMOJI['info']} **Bot Status**\n\n"
        f"🟢 **Status:** Online\n"
        f"⏱️ **Uptime:** {int(uptime // 3600)}h {int((uptime % 3600) // 60)}m\n"
        f"👥 **Active Users:** {len(user_states)}\n"
        f"📊 **Memory Usage:** Working\n\n"
        f"Channel: {CHANNEL_USERNAME}"
    )
    
    bot.reply_to(message, status_text, parse_mode='Markdown')

@bot.message_handler(content_types=['document'])
def handle_document(message):
    """Handle incoming documents"""
    user_id = message.from_user.id
    
    # Check channel membership
    if not is_user_in_channel(user_id):
        bot.reply_to(
            message,
            f"{EMOJI['error']} **Please join our channel first!**\n\n"
            f"📢 {CHANNEL_USERNAME}",
            parse_mode='Markdown'
        )
        return
    
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
        
        user_states[user_id] = 'waiting_for_name'
        
        # Send file info
        info_text = (
            f"{EMOJI['success']} **File Received!**\n\n"
            f"📄 **Name:** `{file_name}`\n"
            f"📦 **Size:** {size_text}\n"
            f"🔖 **Extension:** `{file_ext}`\n"
            f"📋 **Type:** `{mime_type}`\n\n"
            f"{EMOJI['rename']} **Now send me the new name** (without extension):"
        )
        
        bot.reply_to(message, info_text, parse_mode='Markdown')
        logger.info(f"User {user_id} uploaded: {file_name} ({size_text})")
        
    except Exception as e:
        logger.error(f"Error handling document: {e}")
        bot.reply_to(
            message,
            f"{EMOJI['error']} Error processing file. Please try again."
        )

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == 'waiting_for_name')
def handle_new_name(message):
    """Handle new filename from user"""
    user_id = message.from_user.id
    
    try:
        # Get new name
        new_name = message.text.strip()
        
        if not new_name:
            bot.reply_to(
                message,
                f"{EMOJI['error']} Name cannot be empty! Please send a valid name:"
            )
            return
        
        # Validate filename
        if len(new_name) > 100:
            bot.reply_to(
                message,
                f"{EMOJI['error']} Name too long! Max 100 characters. Please try again:"
            )
            return
        
        # Remove invalid characters
        valid_chars = "".join(c for c in new_name if c.isalnum() or c in (' ', '-', '_', '.'))
        
        if not valid_chars:
            bot.reply_to(
                message,
                f"{EMOJI['error']} Invalid characters! Use letters, numbers, spaces, - _ . only.\n"
                f"Please try again:"
            )
            return
        
        # Get file data
        file_data = user_files.get(user_id)
        if not file_data:
            bot.reply_to(
                message,
                f"{EMOJI['error']} Session expired! Please send the file again."
            )
            del user_states[user_id]
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
        del user_states[user_id]
        
        # Ask for next action
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("🔄 Rename Another", callback_data="rename_another")
        btn2 = types.InlineKeyboardButton("❌ Cancel", callback_data="cancel")
        markup.add(btn1, btn2)
        
        bot.send_message(
            user_id,
            f"{EMOJI['done']} **What would you like to do?**",
            parse_mode='Markdown',
            reply_markup=markup
        )
        
        logger.info(f"User {user_id} renamed: {original_name} → {new_filename}")
        
    except Exception as e:
        logger.error(f"Error renaming file: {e}")
        bot.reply_to(
            message,
            f"{EMOJI['error']} Error renaming file. Please try again with /start"
        )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    """Handle inline keyboard callbacks"""
    user_id = call.from_user.id
    
    if call.data == "rename_another":
        bot.edit_message_text(
            f"{EMOJI['file']} **Send me a file to rename!**",
            user_id,
            call.message.message_id,
            parse_mode='Markdown'
        )
    elif call.data == "cancel":
        bot.edit_message_text(
            f"{EMOJI['success']} **Cancelled!**\n\nSend /start to begin again.",
            user_id,
            call.message.message_id,
            parse_mode='Markdown'
        )
    
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    """Handle other messages"""
    user_id = message.from_user.id
    
    if user_states.get(user_id) == 'waiting_for_name':
        bot.reply_to(
            message,
            f"{EMOJI['rename']} Please send the new name for your file:"
        )
    else:
        bot.reply_to(
            message,
            f"{EMOJI['info']} Send me a file to rename it!\n"
            f"Use /start for help."
        )

# Cleanup old data periodically
def cleanup_old_data():
    """Remove old user data"""
    while True:
        try:
            current_time = time.time()
            for user_id in list(user_files.keys()):
                if current_time - user_files[user_id].get('timestamp', 0) > 300:  # 5 minutes
                    del user_files[user_id]
                    if user_id in user_states:
                        del user_states[user_id]
                    logger.info(f"Cleaned up data for user {user_id}")
            time.sleep(60)  # Check every minute
        except Exception as e:
            logger.error(f"Cleanup error: {e}")

# Start cleanup thread
import threading
cleanup_thread = threading.Thread(target=cleanup_old_data, daemon=True)
cleanup_thread.start()

# Record start time
start_time = time.time()

# Main bot loop
if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("🤖 Bot is starting...")
    logger.info(f"📢 Channel: {CHANNEL_USERNAME}")
    logger.info("=" * 50)
    
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=30)
        except Exception as e:
            logger.error(f"Bot crashed: {e}")
            logger.info("Restarting in 5 seconds...")
            time.sleep(5)
