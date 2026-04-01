import telebot
from telebot import types
import yt_dlp
import os
import time
import random
import re
import threading
import json
import requests

# ========== الإعدادات الأساسية ==========
TOKEN = '8505607439:AAEw3-Ci_4yWATze9pfRnzr75ASq4bFpRoE'
INITIAL_LEADER_ID = 123456789  

bot = telebot.TeleBot(TOKEN)
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER): os.makedirs(DOWNLOAD_FOLDER)

# ========== قاعدة البيانات ==========
DATA_FILE = 'war_database.json'
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            if "replies" not in data: data["replies"] = {}
            if "vips" not in data: data["vips"] = []
            if "muted" not in data: data["muted"] = {}
            return data
    return {"owner": INITIAL_LEADER_ID, "admins": [], "vips": [], "replies": {}, "muted": {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f: json.dump(data, f)

db = load_data()

# ========== نظام الصلاحيات ==========
def is_global_owner(user_id): return user_id == db["owner"]
def is_group_admin(chat_id, user_id):
    if is_global_owner(user_id) or user_id in db["admins"]: return True
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['creator', 'administrator']
    except: return False
def is_vip(user_id): return user_id in db["vips"]

# ========== الترحيب بالأعضاء الجدد ==========
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        if new_member.id != bot.get_me().id:
            bot.reply_to(message, f"يا هلا بـ [{new_member.first_name}](tg://user?id={new_member.id})!\nنورت الجروب يا وحش، حياك بكلان WAR CLAN 🦅🔥", parse_mode="Markdown")

# ========== أوامر الإدارة والعقوبات ==========
@bot.message_handler(func=lambda m: m.text and m.text == "مسح مكتومين" and m.chat.type in ['group', 'supergroup'])
def clear_mutes(message):
    chat_id, sender_id = str(message.chat.id), message.from_user.id
    if not is_group_admin(message.chat.id, sender_id): return
    if chat_id in db["muted"] and len(db["muted"][chat_id]) > 0:
        count = 0
        for target_id in db["muted"][chat_id]:
            try:
                bot.restrict_chat_member(chat_id, target_id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True)
                count += 1
            except: pass
        db["muted"][chat_id] = []
        save_data(db); bot.reply_to(message, f"✅ تم فك الكتم عن ({count}) أشخاص!")
    else: bot.reply_to(message, "ماكو مكتومين حالياً.")

@bot.message_handler(func=lambda m: m.text and m.reply_to_message and m.text in ["رفع ادمن", "تنزيل ادمن", "رفع مميز", "تنزيل مميز", "طرد", "حظر", "كتم", "الغاء كتم"])
def admin_commands(message):
    chat_id, sender_id = message.chat.id, message.from_user.id
    target_id = message.reply_to_message.from_user.id
    target_name = f"[{message.reply_to_message.from_user.first_name}](tg://user?id={target_id})"
    cmd = message.text

    if cmd == "رفع ادمن" and is_group_admin(chat_id, sender_id):
        if target_id not in db["admins"]: db["admins"].append(target_id); save_data(db)
        bot.reply_to(message, f"👑 تم رفع {target_name} **أدمن**.", parse_mode="Markdown")
    elif cmd == "تنزيل ادمن" and is_group_admin(chat_id, sender_id):
        if target_id in db["admins"]: db["admins"].remove(target_id)
        if target_id not in db["vips"]: db["vips"].append(target_id)
        save_data(db); bot.reply_to(message, f"🔽 تنزيل {target_name} لـ **عضو مميز**.", parse_mode="Markdown")
    elif cmd == "رفع مميز" and is_group_admin(chat_id, sender_id):
        if target_id not in db["vips"]: db["vips"].append(target_id); save_data(db)
        bot.reply_to(message, f"🌟 رفع {target_name} لـ **مميز**.", parse_mode="Markdown")
    elif cmd == "تنزيل مميز" and is_group_admin(chat_id, sender_id):
        if target_id in db["vips"]: db["vips"].remove(target_id); save_data(db)
        bot.reply_to(message, f"🔽 تنزيل {target_name} لعضو عادي.", parse_mode="Markdown")
    elif cmd == "طرد" and is_group_admin(chat_id, sender_id):
        try: bot.kick_chat_member(chat_id, target_id); bot.unban_chat_member(chat_id, target_id); bot.reply_to(message, f"✈️ طرد {target_name}.")
        except: pass
    elif cmd == "كتم" and (is_group_admin(chat_id, sender_id) or is_vip(sender_id)):
        try:
            bot.restrict_chat_member(chat_id, target_id, can_send_messages=False)
            cid = str(chat_id)
            if cid not in db["muted"]: db["muted"][cid] = []
            if target_id not in db["muted"][cid]: db["muted"][cid].append(target_id)
            save_data(db); bot.reply_to(message, f"🤐 كتم {target_name}.")
        except: pass

# ========== نظام الردود بالميديا ==========
@bot.message_handler(func=lambda m: m.text == "اضف رد" and m.chat.type in ['group', 'supergroup'])
def start_add_reply(message):
    if not is_group_admin(message.chat.id, message.from_user.id): return
    msg = bot.reply_to(message, "دز **الكلمة** اللي تريدني أرد عليها:")
    bot.register_next_step_handler(msg, process_word, message.from_user.id)

def process_word(message, admin_id):
    if message.from_user.id != admin_id: return
    word = message.text
    msg = bot.reply_to(message, f"دز **الرد** مال كلمة '{word}':")
    bot.register_next_step_handler(msg, process_reply, admin_id, word)

def process_reply(message, admin_id, word):
    if message.from_user.id != admin_id: return
    chat_id, r_data = str(message.chat.id), {}
    if message.content_type == 'text': r_data = {"type": "text", "content": message.text}
    elif message.content_type == 'photo': r_data = {"type": "photo", "file_id": message.photo[-1].file_id, "caption": message.caption or ""}
    elif message.content_type == 'video': r_data = {"type": "video", "file_id": message.video.file_id, "caption": message.caption or ""}
    elif message.content_type == 'animation': r_data = {"type": "animation", "file_id": message.animation.file_id, "caption": message.caption or ""}
    elif message.content_type == 'voice': r_data = {"type": "voice", "file_id": message.voice.file_id}
    
    if chat_id not in db["replies"]: db["replies"][chat_id] = {}
    db["replies"][chat_id][word] = r_data
    save_data(db); bot.reply_to(message, f"✅ تم حفظ الرد!")

# ========== العقل المحلي (ردود جاهزة) ==========
def get_instant_reply(text):
    t = text.lower()
    if any(w in t for w in ["اوامر", "أوامر", "/help"]):
        return "🛠 **أوامر بوت WAR CLAN:**\n- `اضف رد` | `الردود`\n- بالرد: `طرد` | `كتم` | `رفع ادمن` | `رفع مميز`"
    if any(w in t for w in ["شلونك", "شخبارك", "شلونكم"]):
        return random.choice(["بخير وعافية يا بطل! 🦅", "الحمدلله يا وحش! 🔥", "بأحسن حال! 👑"])
    if any(w in t for w in ["السلام عليكم", "سلام عليكم"]):
        return "وعليكم السلام يا هلا بيك يا وحش! 👑"
    if any(w in t for w in ["بنورك", "نورك"]):
        return random.choice(["نورك العاكس يا بطل! 🦅", "نورك غطى عالكهرباء 😂👑"])
    if t == "بوت" or "يا بوت" in t:
        return "أنت بوت! 😂"
    return None

# ========== معالج الرسائل العام ==========
@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_all(message):
    chat_id, text = message.chat.id, message.text
    chat_id_str = str(chat_id)
    if chat_id_str in db["replies"] and text in db["replies"][chat_id_str]:
        r = db["replies"][chat_id_str][text]
        if r["type"] == "text": bot.reply_to(message, r["content"])
        elif r["type"] == "photo": bot.send_photo(chat_id, r["file_id"], caption=r["caption"], reply_to_message_id=message.message_id)
        elif r["type"] == "video": bot.send_video(chat_id, r["file_id"], caption=r["caption"], reply_to_message_id=message.message_id)
        elif r["type"] == "voice": bot.send_voice(chat_id, r["file_id"], reply_to_message_id=message.message_id)
        return
    instant = get_instant_reply(text)
    if instant: bot.reply_to(message, instant)

if __name__ == "__main__":
    bot.polling(none_stop=True)
    
