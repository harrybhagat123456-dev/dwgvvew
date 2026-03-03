"""
COMPLETE HANDLER FILE - Add this to your bot
Filename: json_to_txt.py

Commands:
  /json2txt - Convert JSON to clean TXT format

Output format: [CATEGORY] Name:URL
Navigation: Clickable links pointing to first message of each category
"""

import json
import os
import re
from collections import defaultdict
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message


# ============================================================
# CATEGORY TRACKER CLASS
# ============================================================

class CategoryTracker:
    """Track uploads and FIRST message ID of each category"""
    
    def __init__(self):
        self.categories = {}
        self.current_category = None
    
    def set_category(self, category: str):
        self.current_category = category
        if category not in self.categories:
            self.categories[category] = {
                'first_msg_id': None,
                'count': 0,
                'files': []
            }
    
    def add_upload(self, name: str, msg_id: int, file_type: str):
        if self.current_category is None:
            return
        
        cat = self.categories[self.current_category]
        
        # Set FIRST message ID
        if cat['first_msg_id'] is None:
            cat['first_msg_id'] = msg_id
        
        cat['files'].append({
            'name': name,
            'msg_id': msg_id,
            'type': file_type
        })
        cat['count'] += 1
    
    def get_categories(self):
        return self.categories


# ============================================================
# HELPER FUNCTION
# ============================================================

def extract_category_from_link(line: str):
    """Parse: [CATEGORY] Name:URL -> (category, name, url)"""
    match = re.match(r'^\[([^\]]+)\]\s*(.+?):(https?://.+)$', line.strip())
    if match:
        return match.group(1), match.group(2).strip(), match.group(3).strip()
    return None, None, None


# ============================================================
# NAVIGATION INDEX GENERATOR
# ============================================================

async def create_navigation_index(bot, channel_id, tracker, batch_name, credit):
    """Create clickable navigation pointing to first message of each category"""
    
    categories = tracker.get_categories()
    if not categories:
        return None
    
    # Get channel link format
    try:
        chat = await bot.get_chat(channel_id)
        channel_username = chat.username
        channel_id_str = str(channel_id).replace("-100", "")
    except:
        channel_username = None
        channel_id_str = str(channel_id).replace("-100", "")
    
    def get_link(msg_id):
        if channel_username:
            return f"https://t.me/{channel_username}/{msg_id}"
        return f"https://t.me/c/{channel_id_str}/{msg_id}"
    
    # Build navigation
    nav_text = f"<b>📚 {batch_name}</b>\n"
    nav_text += "<b>━━━━━━━━━━━━━━━━━━━━</b>\n"
    nav_text += "<b>📋 CATEGORY INDEX</b>\n"
    nav_text += "<b>━━━━━━━━━━━━━━━━━━━━</b>\n\n"
    nav_text += "<b>🔗 Click to jump to category:</b>\n\n"
    
    total_files = 0
    
    for category in sorted(categories.keys()):
        cat_data = categories[category]
        first_msg_id = cat_data['first_msg_id']
        count = cat_data['count']
        
        if not first_msg_id:
            continue
        
        # Count types
        videos = sum(1 for f in cat_data['files'] if f['type'] == 'video')
        pdfs = sum(1 for f in cat_data['files'] if f['type'] == 'pdf')
        
        type_str = ""
        if videos > 0:
            type_str += f"🎥 {videos} "
        if pdfs > 0:
            type_str += f"📄 {pdfs}"
        
        link = get_link(first_msg_id)
        
        # Clickable category link
        nav_text += f"📂 <a href='{link}'>{category}</a>\n"
        nav_text += f"   └ {type_str.strip()}\n\n"
        
        total_files += count
    
    nav_text += "<b>━━━━━━━━━━━━━━━━━━━━</b>\n"
    nav_text += f"<b>📊 {total_files} files in {len(categories)} categories</b>\n"
    nav_text += f"<b>🌟 {credit}</b>\n"
    
    nav_msg = await bot.send_message(
        chat_id=channel_id,
        text=nav_text,
        disable_web_page_preview=True
    )
    return nav_msg


# ============================================================
# JSON TO TXT HANDLER
# ============================================================

@Client.on_message(filters.command("json2txt") & filters.private)
async def json_to_txt_handler(bot: Client, m: Message):
    """Convert JSON to clean TXT: [CATEGORY] Name:URL"""
    
    editable = await m.reply_text(
        "<b>📤 JSON to TXT Converter</b>\n\n"
        "Send the <b>JSON file</b>\n\n"
        "<i>Output: [CATEGORY] Name:URL</i>"
    )
    
    input_msg = await bot.listen(m.chat.id)
    
    if not input_msg.document or not input_msg.document.file_name.endswith('.json'):
        await m.reply_text("❌ Send valid .json file")
        return
    
    status = await m.reply_text("⏳ Processing...")
    json_path = await input_msg.download()
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # Get batch name
        batch_name = list(json_data.keys())[0]
        batch_data = json_data[batch_name]
        
        output_lines = []
        total = 0
        stats = {}
        
        # Parse JSON structure
        for main_cat, main_data in batch_data.items():
            if not isinstance(main_data, dict):
                continue
            
            for sub_cat, sub_data in main_data.items():
                if not isinstance(sub_data, dict):
                    continue
                
                category_name = sub_cat
                stats[category_name] = 0
                
                # Process all content types
                for content_type in ['videos', 'notes', 'DppNotes', 'DppVideos']:
                    if content_type not in sub_data:
                        continue
                    
                    items = sub_data[content_type]
                    if not isinstance(items, list):
                        continue
                    
                    for item in items:
                        if 'url' not in item:
                            continue
                        
                        url = item['url']
                        name = item.get('name', 'Untitled')
                        
                        # ONLY THIS FORMAT - Clean, no comments
                        output_lines.append(f"[{category_name}] {name}:{url}")
                        total += 1
                        stats[category_name] += 1
                
                if stats[category_name] == 0:
                    del stats[category_name]
        
        # Save
        output_file = f"{batch_name}_categorized.txt"
        output_path = os.path.join("downloads", output_file)
        os.makedirs("downloads", exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))
        
        os.remove(json_path)
        await status.delete()
        
        # Stats
        caption = f"✅ <b>Converted!</b>\n🔗 <b>Total:</b> {total}\n\n"
        for cat, count in sorted(stats.items()):
            caption += f"• {cat}: {count}\n"
        
        await m.reply_document(document=output_path, caption=caption)
        os.remove(output_path)
        
    except Exception as e:
        await m.reply_text(f"❌ Error: {str(e)}")
        if os.path.exists(json_path):
            os.remove(json_path)


# ============================================================
# REGISTER FUNCTION
# ============================================================

def register_json_to_txt(bot):
    """Call this in main.py to register the handler"""
    # Handler is already registered with decorator above
    pass
