import os, re, sys, json, pytz, asyncio, requests, subprocess, random
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, InputMediaPhoto
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
import globals
from logs import logging
from html_handler import register_html_handlers
from drm_handler import register_drm_handlers
from text_handler import register_text_handlers
from features import register_feature_handlers
from upgrade import register_upgrade_handlers
from commands import register_commands_handlers
from settings import register_settings_handlers
from broadcast import register_broadcast_handlers
from youtube_handler import register_youtube_handlers
from authorisation import register_authorisation_handlers
from vars import API_ID, API_HASH, BOT_TOKEN, OWNER, CREDIT, AUTH_USERS, TOTAL_USERS, cookies_file_path
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workdir="."
)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎙️ Commands", callback_data="cmd_command")],
            [InlineKeyboardButton("💎 Features", callback_data="feat_command"), InlineKeyboardButton("⚙️ Settings", callback_data="setttings")],
            [InlineKeyboardButton("💳 Suscribation", callback_data="upgrade_command")],
            [InlineKeyboardButton(text="📞 Contact", url=f"tg://openmessage?user_id={OWNER}"), InlineKeyboardButton(text="🛠️ Repo", url="https://github.com/nikhilsainiop/saini-txt-direct")],
        ])      

@bot.on_message(filters.command("start"))
async def start(bot, m: Message):
    user_id = m.chat.id
    if user_id not in TOTAL_USERS:
        TOTAL_USERS.append(user_id)
    user = await bot.get_me()
    mention = user.mention
    if m.chat.id in AUTH_USERS:
        caption = (
            f"𝐇𝐞𝐥𝐥𝐨 𝐃𝐞𝐚𝐫 👋!\n\n"
            f"➠ 𝐈 𝐚𝐦 𝐚 𝐓𝐞𝐱𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐫 𝐁𝐨𝐭\n\n"
            f"➠ Can Extract Videos & PDFs From Your Text File and Upload to Telegram!\n\n"
            f"➠ For Guide Use button - **✨ Commands** 📖\n\n"
            f"➠ 𝐌𝐚𝐝𝐞 𝐁𝐲 : [{CREDIT}](tg://openmessage?user_id={OWNER}) 🦁"
        )
    else:
        caption = (
            f"𝐇𝐞𝐥𝐥𝐨 **{m.from_user.first_name}** 👋!\n\n"
            f"➠ 𝐈 𝐚𝐦 𝐚 𝐓𝐞𝐱𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐫 𝐁𝐨𝐭\n\n"
            f"➠ Can Extract Videos & PDFs From Your Text File and Upload to Telegram!\n\n"
            f"**You are currently using the free version.** 🆓\n"
            f"**Want to get started? Press /id**\n\n"
            f"💬 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 : [{CREDIT}](tg://openmessage?user_id={OWNER}) to Get The Subscription ! 🔓\n"
        )
    await bot.send_photo(
        chat_id=m.chat.id,
        photo="https://iili.io/KuCBoV2.jpg",
        caption=caption,
        reply_markup=keyboard
    )
    
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("back_to_main_menu"))
async def back_to_main_menu(client, callback_query):
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name
    caption = (
        f"𝐇𝐞𝐥𝐥𝐨 **{first_name}** 👋!\n\n"
        f"➠ 𝐈 𝐚𝐦 𝐚 𝐓𝐞𝐱𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐫 𝐁𝐨𝐭\n\n"
        f"➠ Can Extract Videos & PDFs From Your Text File and Upload to Telegram!\n\n"
        f"╭────────⊰◆⊱────────╮\n"
        f"➠ 𝐌𝐚𝐝𝐞 𝐁𝐲 : [{CREDIT}](tg://openmessage?user_id={OWNER}) 💻\n"
        f"╰────────⊰◆⊱────────╯\n"
    )
    
    await callback_query.message.edit_media(
      InputMediaPhoto(
        media="https://envs.sh/GVI.jpg",
        caption=caption
      ),
      reply_markup=keyboard
    )
    await callback_query.answer()  

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

@bot.on_message(filters.command(["id"]))
async def id_command(client, message: Message):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Send to Owner", url=f"tg://openmessage?user_id={OWNER}")]])
    chat_id = message.chat.id
    text = f"<blockquote expandable><b>The ID of this chat id is:</b></blockquote>\n`{chat_id}`"
    
    if str(chat_id).startswith("-100"):
        await message.reply_text(text)
    else:
        await message.reply_text(text, reply_markup=keyboard)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

@bot.on_message(filters.private & filters.command(["info"]))
async def info(bot: Client, update: Message):
    text = (
        f"╭────────────────╮\n"
        f"│✨ **Your Telegram Info**✨ \n"
        f"├────────────────\n"
        f"├🔹**Name :** `{update.from_user.first_name} {update.from_user.last_name if update.from_user.last_name else 'None'}`\n"
        f"├🔹**User ID :** {('@' + update.from_user.username) if update.from_user.username else 'None'}\n"
        f"├🔹**TG ID :** `{update.from_user.id}`\n"
        f"├🔹**Profile :** {update.from_user.mention}\n"
        f"╰────────────────╯"
    )    
    await update.reply_text(        
        text=text,
        disable_web_page_preview=True
    )

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command(["logs"]))
async def send_logs(client: Client, m: Message):  # Correct parameter name
    try:
        with open("logs.txt", "rb") as file:
            sent = await m.reply_text("**📤 Sending you ....**")
            await m.reply_document(document=file)
            await sent.delete()
    except Exception as e:
        await m.reply_text(f"**Error sending logs:**\n<blockquote>{e}</blockquote>")

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command(["reset"]))
async def restart_handler(_, m):
    if m.chat.id != OWNER:
        return
    else:
        await m.reply_text("𝐁𝐨𝐭 𝐢𝐬 𝐑𝐞𝐬𝐞𝐭𝐢𝐧𝐠...", True)
        os.execl(sys.executable, sys.executable, *sys.argv)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command("stop") & filters.private)
async def cancel_handler(client: Client, m: Message):
    if m.chat.id not in AUTH_USERS:
        print(f"User ID not in AUTH_USERS", m.chat.id)
        await bot.send_message(
            m.chat.id, 
            f"<blockquote>__**Oopss! You are not a Premium member**__\n"
            f"__**Please Upgrade Your Plan**__\n"
            f"__**Send me your user id for authorization**__\n"
            f"__**Your User id** __- `{m.chat.id}`</blockquote>\n\n"
        )
    else:
        if globals.processing_request:
            globals.cancel_requested = True
            await m.reply_text(
                "**🛑 STOP REQUEST RECEIVED**\n\n"
                "**Status:** Process will stop after the current file finishes downloading.\n\n"
                "**Note:** Cannot interrupt file mid-download. Please wait a moment...\n\n"
                "⏳ Waiting for current file to complete..."
            )
        else:
            await m.reply_text("**⚡ No active process to cancel.**")


# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
# JSON TO TXT CONVERTER COMMAND
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command("json2txt") & filters.private)
async def json2txt_handler(bot: Client, m: Message):
    """
    Convert JSON file to TXT format: [CATEGORY] Name:URL
    Supports nested JSON structures and extracts video/PDF links.
    """
    if m.chat.id not in AUTH_USERS:
        await m.reply_text(
            f"<blockquote>__**Oopss! You are not a Premium member**__\n"
            f"__**Please Upgrade Your Plan**__\n"
            f"__**Your User id** __- `{m.chat.id}`</blockquote>\n\n"
        )
        return
    
    # Ask for JSON file
    ask_msg = await m.reply_text(
        "**📤 JSON to TXT Converter**\n\n"
        "Send me a JSON file to convert.\n\n"
        "**Output format:**\n`[CATEGORY] Name:URL`\n\n"
        "Send /cancel to abort."
    )
    
    try:
        # Wait for JSON file
        response: Message = await bot.listen(m.chat.id, timeout=120)
        
        if response.text and response.text.lower() == "/cancel":
            await ask_msg.delete()
            await response.delete()
            return
        
        if not response.document:
            await m.reply_text("**❌ Please send a JSON file!**")
            await ask_msg.delete()
            return
        
        if not response.document.file_name.endswith('.json'):
            await m.reply_text("**❌ File must be a .json file!**")
            await ask_msg.delete()
            return
        
        # Download JSON file
        status_msg = await m.reply_text("**📥 Downloading JSON file...**")
        json_path = await response.download()
        
        # Read and parse JSON
        with open(json_path, 'r', encoding='utf-8') as f:
            try:
                json_data = json.load(f)
            except json.JSONDecodeError as e:
                await status_msg.edit(f"**❌ Invalid JSON file!**\nError: {e}")
                os.remove(json_path)
                return
        
        # Extract links from JSON
        extracted_lines = []
        
        def extract_from_json(data, current_category="General"):
            """Recursively extract links from JSON structure."""
            if isinstance(data, dict):
                # Check for common video/PDF URL fields
                url_fields = ['url', 'link', 'videoUrl', 'video_url', 'pdfUrl', 'pdf_url', 
                              'downloadUrl', 'download_url', 'fileUrl', 'file_url', 'src']
                name_fields = ['name', 'title', 'fileName', 'file_name', 'videoName', 
                               'video_name', 'pdfName', 'pdf_name']
                
                # Get category if available
                category = data.get('category', data.get('subject', data.get('topic', current_category)))
                name = None
                url = None
                
                # Extract name
                for field in name_fields:
                    if field in data and data[field]:
                        name = str(data[field])
                        break
                
                # Extract URL
                for field in url_fields:
                    if field in data and data[field]:
                        url = str(data[field])
                        break
                
                # If we found both name and url
                if name and url:
                    if '://' in url:  # Valid URL check
                        extracted_lines.append(f"[{category}] {name}:{url}")
                
                # Recursively process nested structures
                for key, value in data.items():
                    if key not in url_fields and key not in name_fields:
                        if isinstance(value, (dict, list)):
                            extract_from_json(value, category)
            
            elif isinstance(data, list):
                for item in data:
                    extract_from_json(item, current_category)
        
        # Process JSON data
        extract_from_json(json_data)
        
        if not extracted_lines:
            await status_msg.edit("**❌ No valid links found in JSON file!**\n\nMake sure the JSON contains URL fields like 'url', 'videoUrl', 'pdfUrl', etc.")
            os.remove(json_path)
            return
        
        # Create output TXT file
        output_filename = os.path.splitext(response.document.file_name)[0] + ".txt"
        output_path = os.path.join(os.path.dirname(json_path), output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(extracted_lines))
        
        # Send the TXT file
        await status_msg.edit(f"**✅ Conversion Complete!**\n\n"
                              f"**Total links extracted:** {len(extracted_lines)}\n\n"
                              f"**Sending file...**")
        
        await m.reply_document(
            document=output_path,
            caption=f"**📄 JSON → TXT Conversion**\n\n"
                    f"**Total Links:** {len(extracted_lines)}\n"
                    f"**Format:** `[CATEGORY] Name:URL`"
        )
        
        # Cleanup
        os.remove(json_path)
        os.remove(output_path)
        await ask_msg.delete()
        await response.delete()
        await status_msg.delete()
        
    except asyncio.TimeoutError:
        await ask_msg.edit("**⏰ Timeout! Please try again.**")
    except Exception as e:
        await m.reply_text(f"**❌ Error:**\n<blockquote>{str(e)}</blockquote>")


#=================================================================

register_text_handlers(bot)
register_html_handlers(bot)
register_feature_handlers(bot)
register_settings_handlers(bot)
register_upgrade_handlers(bot)
register_commands_handlers(bot)
register_broadcast_handlers(bot)
register_youtube_handlers(bot)
register_authorisation_handlers(bot)
register_drm_handlers(bot)
#==================================================================

def notify_owner():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": OWNER,
        "text": "𝐁𝐨𝐭 𝐑𝐞𝐬𝐭𝐚𝐫𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 ✅"
    }
    requests.post(url, data=data)

def reset_and_set_commands():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands"

    # General users ke liye commands
    general_commands = [
        {"command": "start", "description": "✅ Check Alive the Bot"},
        {"command": "stop", "description": "🚫 Stop the ongoing process"},
        {"command": "id", "description": "🆔 Get Your ID"},
        {"command": "info", "description": "ℹ️ Check Your Information"},
        {"command": "cookies", "description": "📁 Upload YT Cookies"},
        {"command": "y2t", "description": "🔪 YouTube → .txt Converter"},
        {"command": "ytm", "description": "🎶 YouTube → .mp3 downloader"},
        {"command": "t2t", "description": "📟 Text → .txt Generator"},
        {"command": "t2h", "description": "🌐 .txt → .html Converter"},
        {"command": "json2txt", "description": "📄 JSON → .txt Converter"},
        {"command": "logs", "description": "👁️ View Bot Activity"},
    ]
    # Owner ke liye extra commands
    owner_commands = general_commands + [
        {"command": "broadcast", "description": "📢 Broadcast to All Users"},
        {"command": "broadusers", "description": "👨‍❤️‍👨 All Broadcasting Users"},
        {"command": "addauth", "description": "▶️ Add Authorisation"},
        {"command": "rmauth", "description": "⏸️ Remove Authorisation "},
        {"command": "users", "description": "👨‍👨‍👧‍👦 All Premium Users"},
        {"command": "reset", "description": "✅ Reset the Bot"}
    ]

    # General users ke liye set commands (scope default)
    requests.post(url, json={
        "commands": general_commands,
        "scope": {"type": "default"},
        "language_code": "en"
    })

    # Owner ke liye set commands (scope user)
    requests.post(url, json={
        "commands": owner_commands,
        "scope": {"type": "chat", "chat_id": OWNER},  # OWNER variable me chat id hona chahiye
        "language_code": "en"
    })
    
if __name__ == "__main__":
    reset_and_set_commands()
    notify_owner() 

bot.run()
