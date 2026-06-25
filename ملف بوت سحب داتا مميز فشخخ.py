#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot
import sqlite3
import os
import threading
import time
import random
from telebot import types
from datetime import datetime

# ==================== CONFIG ====================
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8787220449:AAENYYlOoHbfoTZymkGss5EsBgn3U0FGKiM')
DEVELOPER_ID = int(os.environ.get('DEVELOPER_ID', '7654693261'))

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')

# ==================== CUSTOM EMOJI + AUTO-BLOCKQUOTE ====================
# كل نص يُرسل يُغلَّف تلقائياً في اقتباس وتُستبدل الإيموجي بالمخصصة

_CE = {
    # ✅ check/verify
    '✅': '<tg-emoji emoji-id="6258259403200270844">✅</tg-emoji>',
    '☑️': '<tg-emoji emoji-id="4945049066271671758">☑️</tg-emoji>',
    # 🔍 search
    '🔍': '<tg-emoji emoji-id="5965466792527666087">🔍</tg-emoji>',
    '🔎': '<tg-emoji emoji-id="5965466792527666087">🔎</tg-emoji>',
    # 👤 account
    '👤': '<tg-emoji emoji-id="5373020661574826232">👤</tg-emoji>',
    # 📱 vodafone / mobile
    '📱': '<tg-emoji emoji-id="5834628314731387616">📱</tg-emoji>',
    # 💳 buy/charge
    '💳': '<tg-emoji emoji-id="5447453226498552490">💳</tg-emoji>',
    # 🔗 link/referral
    '🔗': '<tg-emoji emoji-id="5967301267549068409">🔗</tg-emoji>',
    # 🎟 coupon
    '🎟': '<tg-emoji emoji-id="5785167918027250397">🎟</tg-emoji>',
    '🎟️': '<tg-emoji emoji-id="5785167918027250397">🎟️</tg-emoji>',
    # ⚙️ admin/settings
    '⚙️': '<tg-emoji emoji-id="5857054220179480029">⚙️</tg-emoji>',
    # ➕ add
    '➕': '<tg-emoji emoji-id="5857339990123486296">➕</tg-emoji>',
    # 📋 channels/list
    '📋': '<tg-emoji emoji-id="5803363345113290876">📋</tg-emoji>',
    # 🗑 delete
    '🗑': '<tg-emoji emoji-id="5920209833071482745">🗑</tg-emoji>',
    '🗑️': '<tg-emoji emoji-id="5920209833071482745">🗑️</tg-emoji>',
    # ❌ clear/cancel
    '❌': '<tg-emoji emoji-id="5796291784539639311">❌</tg-emoji>',
    # 🛡 promote admin
    '🛡': '<tg-emoji emoji-id="5920298756074379058">🛡</tg-emoji>',
    '🛡️': '<tg-emoji emoji-id="5920298756074379058">🛡️</tg-emoji>',
    # 👥 admins list / referral
    '👥': '<tg-emoji emoji-id="6001388309853510348">👥</tg-emoji>',
    # 🚫 ban
    '🚫': '<tg-emoji emoji-id="5888789252493283486">🚫</tg-emoji>',
    # 🔓 unban
    '🔓': '<tg-emoji emoji-id="5998940732545571769">🔓</tg-emoji>',
    # ➕ add points (16)
    # ➖ subtract points
    '➖': '<tg-emoji emoji-id="5280753674451175517">➖</tg-emoji>',
    # 🔄 reset / ref points
    '🔄': '<tg-emoji emoji-id="5976831692604709621">🔄</tg-emoji>',
    # 💰 search cost / price
    '💰': '<tg-emoji emoji-id="6037182124916740433">💰</tg-emoji>',
    # 🎁 coupon make / confirm
    '🎁': '<tg-emoji emoji-id="5976317950091598658">🎁</tg-emoji>',
    # 🔙 back
    '🔙': '<tg-emoji emoji-id="5253743295141538873">🔙</tg-emoji>',
    # ✨ extra / orange
    '✨': '<tg-emoji emoji-id="5254001839287859496">✨</tg-emoji>',
    # 📊 stats
    '📊': '<tg-emoji emoji-id="5935935761336505948">📊</tg-emoji>',
    # 📢 broadcast
    '📢': '<tg-emoji emoji-id="5902385465390013835">📢</tg-emoji>',
    # 🌐 WE
    '🌐': '<tg-emoji emoji-id="5837128389424585193">🌐</tg-emoji>',
    # 🧙 natera
    '🧙': '<tg-emoji emoji-id="5803157577525106419">🧙</tg-emoji>',
    # 📡 etisalat
    '📡': '<tg-emoji emoji-id="5836811137370297987">📡</tg-emoji>',
    # 🌾 tamween
    '🌾': '<tg-emoji emoji-id="5981216003810400332">🌾</tg-emoji>',
    # 🛠 support
    '🛠': '<tg-emoji emoji-id="5965466792527666087">🛠</tg-emoji>',
    '🛠️': '<tg-emoji emoji-id="5965466792527666087">🛠️</tg-emoji>',
    # 👑 crown
    '👑': '<tg-emoji emoji-id="5319149831673887746">👑</tg-emoji>',
    # 🆕 new
    '🆕': '<tg-emoji emoji-id="5857339990123486296">🆕</tg-emoji>',
    # 📤 upload
    '📤': '<tg-emoji emoji-id="5920298756074379058">📤</tg-emoji>',
    # 📥 download
    '📥': '<tg-emoji emoji-id="5920415115328362511">📥</tg-emoji>',
    # 📞 phone
    '📞': '<tg-emoji emoji-id="5373020661574826232">📞</tg-emoji>',
    # 🏦 bank
    '🏦': '<tg-emoji emoji-id="5803363345113290876">🏦</tg-emoji>',
    # 💎 diamond / vip
    '💎': '<tg-emoji emoji-id="5254001839287859496">💎</tg-emoji>',
    # 🔑 key
    '🔑': '<tg-emoji emoji-id="5785167918027250397">🔑</tg-emoji>',
    # 🎫 ticket
    '🎫': '<tg-emoji emoji-id="5785167918027250397">🎫</tg-emoji>',
    # 📌 pin
    '📌': '<tg-emoji emoji-id="5920298756074379058">📌</tg-emoji>',
    # 📝 memo
    '📝': '<tg-emoji emoji-id="5314299563761222650">📝</tg-emoji>',
    # 📈 chart up
    '📈': '<tg-emoji emoji-id="5935935761336505948">📈</tg-emoji>',
    # 📅 calendar
    '📅': '<tg-emoji emoji-id="5314299563761222650">📅</tg-emoji>',
    # 📦 package
    '📦': '<tg-emoji emoji-id="5881760620117760960">📦</tg-emoji>',
    # 🔢 numbers
    '🔢': '<tg-emoji emoji-id="5965466792527666087">🔢</tg-emoji>',
    # ✏️ pencil
    '✏️': '<tg-emoji emoji-id="5314299563761222650">✏️</tg-emoji>',
    # 🖨 printer
    '🖨': '<tg-emoji emoji-id="5967617875358258757">🖨</tg-emoji>',
    '🖨️': '<tg-emoji emoji-id="5967617875358258757">🖨️</tg-emoji>',
    # 🖼 picture
    '🖼': '<tg-emoji emoji-id="5294079682365384341">🖼</tg-emoji>',
    '🖼️': '<tg-emoji emoji-id="5294079682365384341">🖼️</tg-emoji>',
    # ⏳ hourglass
    '⏳': '<tg-emoji emoji-id="5314299563761222650">⏳</tg-emoji>',
    # ⏰ alarm
    '⏰': '<tg-emoji emoji-id="5314299563761222650">⏰</tg-emoji>',
    # 🎉 party
    '🎉': '<tg-emoji emoji-id="5254001839287859496">🎉</tg-emoji>',
    # 🔹 small diamond blue
    '🔹': '<tg-emoji emoji-id="5967301267549068409">🔹</tg-emoji>',
    # ⭐ star
    '⭐': '<tg-emoji emoji-id="5254001839287859496">⭐</tg-emoji>',
    # 😎 sunglasses
    '😎': '<tg-emoji emoji-id="5976308930660276596">😎</tg-emoji>',
    # 💗 heart
    '💗': '<tg-emoji emoji-id="6043941205144771802">💗</tg-emoji>',
    # 🎯 target
    '🎯': '<tg-emoji emoji-id="5965466792527666087">🎯</tg-emoji>',
    # 📂 folder
    '📂': '<tg-emoji emoji-id="5881760620117760960">📂</tg-emoji>',
    # 🗂 card index
    '🗂': '<tg-emoji emoji-id="5881760620117760960">🗂</tg-emoji>',
    '🗂️': '<tg-emoji emoji-id="5881760620117760960">🗂️</tg-emoji>',
    # 💲 dollar
    '💲': '<tg-emoji emoji-id="6003691769533829755">💲</tg-emoji>',
    # ⚠️ warning
    '⚠️': '<tg-emoji emoji-id="5999278377104578246">⚠️</tg-emoji>',
    # 🔴 red circle
    '🔴': '<tg-emoji emoji-id="5999278377104578246">🔴</tg-emoji>',
    # 🟢 green circle
    '🟢': '<tg-emoji emoji-id="4945049066271671758">🟢</tg-emoji>',
    # 🔵 blue circle
    '🔵': '<tg-emoji emoji-id="5967301267549068409">🔵</tg-emoji>',
    # 💬 speech bubble
    '💬': '<tg-emoji emoji-id="5314299563761222650">💬</tg-emoji>',
    # 🧹 broom
    '🧹': '<tg-emoji emoji-id="5920415115328362511">🧹</tg-emoji>',
    # ⬆️ up arrow
    '⬆️': '<tg-emoji emoji-id="5920298756074379058">⬆️</tg-emoji>',
    # ⬇️ down arrow
    '⬇️': '<tg-emoji emoji-id="5922681088534124293">⬇️</tg-emoji>',
    # 🏷 label
    '🏷': '<tg-emoji emoji-id="5881760620117760960">🏷</tg-emoji>',
    '🏷️': '<tg-emoji emoji-id="5881760620117760960">🏷️</tg-emoji>',
    # 📣 megaphone
    '📣': '<tg-emoji emoji-id="5902385465390013835">📣</tg-emoji>',
    # 🎨 palette
    '🎨': '<tg-emoji emoji-id="5254001839287859496">🎨</tg-emoji>',
}


def _apply_ce(text: str) -> str:
    """استبدال الإيموجي العادية بالإيموجي المخصصة."""
    if not text:
        return text
    for ch, replacement in _CE.items():
        text = text.replace(ch, replacement)
    return text


def _bq(text: str) -> str:
    """تغليف النص في اقتباس مع تطبيق الإيموجي المخصصة."""
    return f"<blockquote>{_apply_ce(str(text))}</blockquote>"


# ── Monkey-patch: كل رسالة تُرسل تلقائياً في اقتباس بإيموجي مخصصة ──
_orig_send_msg   = bot.send_message
_orig_send_photo = bot.send_photo
_orig_edit_text  = bot.edit_message_text
_orig_edit_cap   = bot.edit_message_caption


def _send_message(chat_id, text, **kw):
    kw.setdefault('parse_mode', 'HTML')
    return _orig_send_msg(chat_id, _bq(text), **kw)


def _send_photo(chat_id, photo, caption=None, **kw):
    kw.setdefault('parse_mode', 'HTML')
    return _orig_send_photo(chat_id, photo,
                            caption=_bq(caption) if caption else None, **kw)


def _edit_message_text(text, chat_id=None, message_id=None, **kw):
    kw.setdefault('parse_mode', 'HTML')
    return _orig_edit_text(_bq(text), chat_id=chat_id,
                           message_id=message_id, **kw)


def _edit_message_caption(chat_id=None, message_id=None, caption=None, **kw):
    kw.setdefault('parse_mode', 'HTML')
    return _orig_edit_cap(chat_id=chat_id, message_id=message_id,
                          caption=_bq(caption) if caption else None, **kw)


bot.send_message         = _send_message
bot.send_photo           = _send_photo
bot.edit_message_text    = _edit_message_text
bot.edit_message_caption = _edit_message_caption

# ==================== DATABASE ====================
DB_PATH = 'bot_database.db'


def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        username TEXT,
        first_name TEXT,
        joined_at TEXT DEFAULT CURRENT_TIMESTAMP,
        referred_by INTEGER DEFAULT NULL,
        is_banned INTEGER DEFAULT 0
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        service_key TEXT,
        service_name TEXT,
        service_code TEXT,
        quantity INTEGER,
        price REAL,
        wallet_num TEXT,
        wallet_name TEXT,
        target_num TEXT,
        receipt_file_id TEXT,
        status TEXT DEFAULT 'pending',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        section_order_id INTEGER DEFAULT 1
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        ticket_type TEXT,
        message TEXT,
        status TEXT DEFAULT 'open',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS ticket_photos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id INTEGER,
        file_id TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id TEXT,
        channel_name TEXT,
        sub_type TEXT DEFAULT 'telegram'
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS admins (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        admin_type TEXT DEFAULT 'full',
        added_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS section_admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        section TEXT,
        added_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    # Add captcha_passed column if not exists
    try:
        c.execute('ALTER TABLE users ADD COLUMN captcha_passed INTEGER DEFAULT 0')
    except Exception:
        pass

    # Add service prices table
    c.execute('''CREATE TABLE IF NOT EXISTS service_prices (
        service_key TEXT PRIMARY KEY,
        price REAL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS dynamic_sections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        section_name TEXT,
        welcome_text TEXT DEFAULT '',
        position TEXT DEFAULT 'after',
        is_locked INTEGER DEFAULT 0,
        color TEXT DEFAULT 'none',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS dynamic_buttons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        section_id INTEGER,
        button_name TEXT,
        service_price REAL DEFAULT 0,
        transfer_num TEXT DEFAULT '',
        service_code TEXT DEFAULT '',
        welcome_text TEXT DEFAULT '',
        is_locked INTEGER DEFAULT 0,
        color TEXT DEFAULT 'none'
    )''')

    conn.commit()

    defaults = {
        'welcome_text': (
            '👑 مـرحبآ بڪ أيها الـعـمـيل {name} 👑\n\n'
            'انت الان فـ بوت سحب بـيـانـات الـرقم\n'
            'الـخـاص بـ مـنـظـمـة X • X ✅\n\n'
            'قـوانـيـن الـبـوت لـتـجـنـب الـحظر كـالـتـالي 🛡️:\n\n'
            '1 - عـدم تـكـرار إرسـال الـطـلـب 🛡️\n'
            '2 - إرسـال الـطـلـب بـ مـتـطـلبـات \nالـقـسـم الـخـاص بـه 🛡️\n'
            '3 - عـدم إرسـال اسـم / رقـم الـمـحـفـظـه 💳\n'
            '4 - إسـتـعـجالـك لـلـطـلـب 🚫\n'
            '5 - إرسـال رسـائـل لـتـخـص غـرض\nالـبـوت فـ قـسـم الـدعـم الفني 🛡️\n'
            'هـذي كـانـت قـوانـيـن الـبـوت .🛡️\n\n'
            'طـريـقـة إسـتـخـدام الـبـوت ✅\n\n'
            '1 - إرسـال اسـكـريـن الـتـحـويـل 🛡️\n'
            '2 - إرسـال رقـم الـمـحـفـظـه\nالـمُـحـول مـنـهـا 🔥\n'
            '3 - إرسـال اسـم الـمـحـفـظـه \nالـمُـحـول مـنـهـا 🏦\n'
            '4 - إرسـال الـرقـم الـمـرغـوب \nالـسـحـب عـلـية 🛡️\n\n'
            'ثُـم تـحـلـي بـالـصـبر 😎\n'
            'وصـلـي عـلـي خـيـر البريه 💗'
        ),
        'welcome_image': 'https://b.top4top.io/p_3791mznyg0.jpg',
        'support_username': '@support',
        'global_transfer_num': '01214691014',
        'trust_channel_id': '',
    }
    for key, value in defaults.items():
        c.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (key, value))

    c.execute('INSERT OR IGNORE INTO admins (user_id, username) VALUES (?, ?)', (DEVELOPER_ID, 'developer'))

    conn.commit()
    conn.close()


# ==================== HELPERS ====================

def get_setting(key, default=''):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT value FROM settings WHERE key = ?', (key,))
    row = c.fetchone()
    conn.close()
    return row['value'] if row else default


def set_setting(key, value):
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, str(value)))
    conn.commit()
    conn.close()


def is_admin(user_id):
    if user_id == DEVELOPER_ID:
        return True
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT user_id FROM admins WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    return row is not None


def is_section_admin(user_id, section):
    if is_admin(user_id):
        return True
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id FROM section_admins WHERE user_id = ? AND section = ?', (user_id, section))
    row = c.fetchone()
    conn.close()
    return row is not None


def has_passed_captcha(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT captcha_passed FROM users WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    return row and row['captcha_passed'] == 1


def mark_captcha_passed(user_id):
    conn = get_db()
    conn.execute('UPDATE users SET captcha_passed = 1 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()


def get_service_price(service_key):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT price FROM service_prices WHERE service_key = ?', (service_key,))
    row = c.fetchone()
    conn.close()
    if row:
        return row['price']
    return SERVICES.get(service_key, {}).get('price', 0)


def get_user_info(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    order_count = c.execute('SELECT COUNT(*) as cnt FROM orders WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()
    return row, order_count['cnt'] if order_count else 0


def get_banned_users():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT user_id, username, first_name FROM users WHERE is_banned = 1')
    rows = c.fetchall()
    conn.close()
    return rows


def check_user_banned(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT is_banned FROM users WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    return row and row['is_banned'] == 1


def add_user(user_id, username, first_name, referred_by=None):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    existing = c.fetchone()
    is_new = existing is None
    if is_new:
        c.execute(
            'INSERT OR IGNORE INTO users (user_id, username, first_name, referred_by) VALUES (?, ?, ?, ?)',
            (user_id, username or '', first_name or '', referred_by)
        )
        conn.commit()
    conn.close()
    return is_new


def get_user_count():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) as cnt FROM users')
    row = c.fetchone()
    conn.close()
    return row['cnt']


def get_subscriptions():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM subscriptions')
    rows = c.fetchall()
    conn.close()
    return rows


def check_subscription(user_id):
    subs = get_subscriptions()
    if not subs:
        return True, []
    not_subscribed = []
    for sub in subs:
        if sub['sub_type'] == 'telegram':
            try:
                member = bot.get_chat_member(sub['channel_id'], user_id)
                if member.status in ['left', 'kicked']:
                    not_subscribed.append(sub)
            except Exception:
                pass
        # URL type cannot be verified programmatically
    return len(not_subscribed) == 0, not_subscribed


def get_section_order_id(service_code):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) as cnt FROM orders WHERE service_code = ?', (service_code,))
    row = c.fetchone()
    conn.close()
    return row['cnt'] + 1


def save_order(user_id, service_key, service_name, service_code,
               quantity, price, wallet_num, wallet_name, target_num, receipt_file_id):
    conn = get_db()
    c = conn.cursor()
    section_id = get_section_order_id(service_code)
    c.execute(
        '''INSERT INTO orders
           (user_id, service_key, service_name, service_code, quantity, price,
            wallet_num, wallet_name, target_num, receipt_file_id, section_order_id)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (user_id, service_key, service_name, service_code, quantity, price,
         wallet_num, wallet_name, target_num, receipt_file_id, section_id)
    )
    order_id = c.lastrowid
    conn.commit()
    conn.close()
    return order_id, section_id


def get_pending_orders_by_section():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT service_code, COUNT(*) as cnt FROM orders WHERE status='pending' GROUP BY service_code")
    rows = c.fetchall()
    conn.close()
    return {row['service_code']: row['cnt'] for row in rows}


def get_all_orders_count():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) as cnt FROM orders')
    row = c.fetchone()
    conn.close()
    return row['cnt']


def get_accepted_orders_count():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) as cnt FROM orders WHERE status='accepted'")
    row = c.fetchone()
    conn.close()
    return row['cnt']


def get_referral_count(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) as cnt FROM users WHERE referred_by = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    return row['cnt']


def get_section_image(section_key):
    """إرجاع صورة القسم المخصصة أو الصورة الافتراضية إن لم توجد."""
    section_img = get_setting(f'image_{section_key}', '')
    if section_img:
        return section_img
    return get_setting('welcome_image', 'https://b.top4top.io/p_3791mznyg0.jpg')


def post_to_trust_channel(order_row, client_name, rating_emoji):
    """نشر إشعار التسليم في قناة الثقة."""
    trust_channel = get_setting('trust_channel_id', '')
    if not trust_channel:
        return
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%I:%M %p').replace('AM', 'ص').replace('PM', 'م')
    service_name = order_row['service_name'] if order_row['service_name'] else order_row['service_code']
    msg = (
        "✅ <b>تم تسليم طلب جديد</b>\n\n"
        "<blockquote>"
        f"🔹 الخدمة : «{service_name}»\n"
        f"🔹 اسم العميل : «{client_name}»\n"
        f"🔹 التاريخ : «{date_str}»\n"
        f"🔹 تقييم الخدمة : {rating_emoji}"
        "</blockquote>"
    )
    section_key = order_row['service_code'].lower().replace('_data', '').replace('etisalat_data', 'etisalat')
    image_url = get_setting(f'image_{section_key}', '') or get_setting('welcome_image', '')
    try:
        if image_url:
            bot.send_photo(trust_channel, image_url, caption=msg, parse_mode='HTML')
        else:
            bot.send_message(trust_channel, msg, parse_mode='HTML')
    except Exception:
        try:
            bot.send_message(trust_channel, msg, parse_mode='HTML')
        except Exception:
            pass


def get_last_referral(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT joined_at FROM users WHERE referred_by = ? ORDER BY joined_at DESC LIMIT 1', (user_id,))
    row = c.fetchone()
    conn.close()
    return row['joined_at'] if row else 'لا يوجد'


def get_transfer_num(section):
    defaults = {
        'vodafone': '01214691014',
        'we': '01214691014',
        'etisalat': '01214691014',
        'tamween': '01214691014',
        'natera': '01559376830',
        'orange': '01559376830',
    }
    return get_setting(f'cash_{section}', defaults.get(section, '01214691014'))


# ==================== CUSTOM EMOJI IDs ====================
EMOJI = [
    "4945049066271671758",   # 0  - check/verify
    "5965466792527666087",   # 1  - search
    "5373020661574826232",   # 2  - account
    "5967507756691757055",   # 3  - buy/charge
    "5967301267549068409",   # 4  - link/referral
    "5785167918027250397",   # 5  - coupon
    "5857054220179480029",   # 6  - admin/settings
    "5857339990123486296",   # 7  - add
    "5881760620117760960",   # 8  - channels/list
    "5920209833071482745",   # 9  - delete
    "5920415115328362511",   # 10 - clear
    "5920298756074379058",   # 11 - promote admin
    "5922681088534124293",   # 12 - demote admin
    "6001388309853510348",   # 13 - admins list
    "5999278377104578246",   # 14 - ban
    "5998940732545571769",   # 15 - unban
    "6003691769533829755",   # 16 - add points
    "5280753674451175517",   # 17 - subtract points
    "5314299563761222650",   # 18 - ref points
    "6037182124916740433",   # 19 - search cost
    "5976317950091598658",   # 20 - coupon make
    "5976831692604709621",   # 21 - reset points
    "5253743295141538873",   # 22 - back
    "5254001839287859496",   # 23 - extra
]
E_STATS    = "5935935761336505948"
E_BCAST    = "5902385465390013835"
E_VODAFONE = "5834628314731387616"
E_WE       = "5837128389424585193"
E_NATERA   = "5316653334688446735"
E_ORANGE   = "5836714629455157161"
E_ETISALAT = "5836811137370297987"
E_TAMWEEN  = "5981216003810400332"
E_ORDERS   = "5907001756369296257"
E_REFERRAL = "5319070993254201336"
E_SUPPORT  = "5316653334688446735"
E_CONFIRM  = "5987615535146210396"
E_CANCEL   = "5330237710655306682"
E_BACK     = "6258259403200270844"

# ==================== SERVICES CONFIG ====================
SERVICES = {
    'vodafone_data': {
        'name': 'سحب بيانات فودافون',
        'emoji': '📱',
        'price': 35.0,
        'section': 'vodafone',
        'service_code': 'vodafone_data',
        'target_prompt': '📞 أرسل الرقم الهدف الآن:\n(بدون فراغات بين الأرقام، ولا يبدأ بـ +2)',
        'quantity_label': 'رقم'
    },
    'vodafone_vip': {
        'name': 'بيانات لرقم مميز فودافون',
        'emoji': '💎',
        'price': 45.0,
        'section': 'vodafone',
        'service_code': 'vodafone_vip',
        'target_prompt': '📞 أرسل الرقم الهدف الآن:\n(بدون فراغات بين الأرقام، ولا يبدأ بـ +2)',
        'quantity_label': 'رقم'
    },
    'vodafone_ownership': {
        'name': 'سحب ملكية سابقة 010',
        'emoji': '🔑',
        'price': 50.0,
        'section': 'vodafone',
        'service_code': 'vodafone_ownership',
        'target_prompt': '📞 أرسل الرقم الهدف الآن:\n(بدون فراغات بين الأرقام، ولا يبدأ بـ +2)',
        'quantity_label': 'رقم'
    },
    'we_cards': {
        'name': 'سحب بطايق 015',
        'emoji': '🔑',
        'price': 50.0,
        'section': 'we',
        'service_code': 'we_data',
        'target_prompt': '📞 أرسل رقم القومي الهدف الآن:\n(بدون فراغات بين الأرقام، ولا يبدأ 0)',
        'quantity_label': 'رقم'
    },
    'we_data': {
        'name': 'سحب بيانات 015',
        'emoji': '🔑',
        'price': 50.0,
        'section': 'we',
        'service_code': 'we',
        'target_prompt': '📞 أرسل رقم القومي الهدف الآن:\n(بدون فراغات بين الأرقام، ولا يبدأ 0)',
        'quantity_label': 'رقم'
    },
    'natera_numbers': {
        'name': 'أرقام نترا',
        'emoji': '📱',
        'price': 60.0,
        'section': 'natera',
        'service_code': 'natera',
        'target_prompt': '📞 أرسل رقم القومي الهدف الآن:\n(بدون فراغات بين الأرقام، ولا يبدأ 0)',
        'quantity_label': 'رقم قومي'
    },
    'orange_data': {
        'name': 'بيانات اورنج',
        'emoji': '📱',
        'price': 60.0,
        'section': 'orange',
        'service_code': 'orange',
        'target_prompt': '📞 أرسل رقم الهدف الآن:\n(بدون فراغات بين الأرقام، ولا يبدأ +2)',
        'quantity_label': 'رقم قومي'
    },
    'orange_open_cache': {
        'name': 'فتح كاشات اورنج',
        'emoji': '🔓',
        'price': 50.0,
        'section': 'orange',
        'service_code': 'orange_open_cache',
        'target_prompt': '📞 أرسل رقم الهدف الآن:\n(بدون فراغات بين الأرقام، ولا يبدأ +2)',
        'quantity_label': 'رقم'
    },
    'orange_close_cache': {
        'name': 'قفل كاشات اورنج',
        'emoji': '🔑',
        'price': 50.0,
        'section': 'orange',
        'service_code': 'orange_close_cache',
        'target_prompt': '📞 أرسل رقم الهدف الآن:\n(بدون فراغات بين الأرقام، ولا يبدأ +2)',
        'quantity_label': 'رقم'
    },
    'etisalat_data': {
        'name': 'سحب بيانات اتصالات',
        'emoji': '📱',
        'price': 35.0,
        'section': 'etisalat',
        'service_code': 'Etisalat_data',
        'target_prompt': '📞 أرسل الرقم الهدف الآن:\n(بدون فراغات بين الأرقام، ولا يبدأ بـ +2)',
        'quantity_label': 'رقم'
    },
    'tamween': {
        'name': 'سحب تموين من رقم القومي',
        'emoji': '🔑',
        'price': 50.0,
        'section': 'tamween',
        'service_code': 'tamween',
        'target_prompt': '📞 أرسل رقم القومي الهدف الآن:\n(بدون فراغات بين الأرقام، ولا يبدأ 0)',
        'quantity_label': 'رقم'
    },
}

# ==================== STATE MANAGEMENT ====================
user_states = {}
captcha_data = {}
countdown_timers = {}


def set_state(user_id, state, **data):
    if user_id not in user_states:
        user_states[user_id] = {'state': state, 'data': {}}
    else:
        user_states[user_id]['state'] = state
    user_states[user_id]['data'].update(data)


def get_state(user_id):
    return user_states.get(user_id, {}).get('state', 'idle')


def get_data(user_id, key, default=None):
    return user_states.get(user_id, {}).get('data', {}).get(key, default)


def clear_state(user_id):
    user_states.pop(user_id, None)


# ==================== COUNTDOWN TIMER ====================

def cancel_countdown(user_id):
    if user_id in countdown_timers:
        try:
            countdown_timers[user_id].cancel()
        except Exception:
            pass
        countdown_timers.pop(user_id, None)


def start_countdown(chat_id, user_id, message_id, has_photo, order_data):
    def update_timer(remaining):
        if user_id not in countdown_timers:
            return
        if get_state(user_id) != 'await_confirm':
            countdown_timers.pop(user_id, None)
            return
        if remaining <= 0:
            # Time expired - auto send to developer
            countdown_timers.pop(user_id, None)
            expired_text = "⏰ انتهى الوقت! تم إرسال طلبك تلقائياً للمراجعة."
            try:
                if has_photo:
                    bot.edit_message_caption(chat_id, message_id, caption=expired_text)
                else:
                    bot.edit_message_text(expired_text, chat_id, message_id)
            except Exception:
                pass
            notify_developer_order(chat_id, user_id, order_data)
            clear_state(user_id)
            return

        mins = remaining // 60
        secs = remaining % 60
        timer_text = f"⏱ {mins:02d}:{secs:02d}"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(timer_text, callback_data="noop"))
        markup.add(
            types.InlineKeyboardButton("✅ تأكيد", callback_data=f"confirm_order_{order_data['service_key']}"),
            types.InlineKeyboardButton("❌ رفض الطلب", callback_data="cancel_order")
        )
        try:
            bot.edit_message_reply_markup(chat_id, message_id, reply_markup=markup)
        except Exception:
            pass

        sleep_time = min(10, remaining)
        t = threading.Timer(sleep_time, update_timer, args=[remaining - sleep_time])
        countdown_timers[user_id] = t
        t.start()

    t = threading.Timer(10, update_timer, args=[110])
    countdown_timers[user_id] = t
    t.start()


def notify_developer_order(chat_id, user_id, order_data):
    service = order_data['service']
    order_id = order_data['order_id']
    section_id = order_data['section_id']
    text = (
        f"🆕 <b>طلب جديد</b>\n\n"
        f"👤 المستخدم: <a href='tg://user?id={user_id}'>{user_id}</a>\n"
        f"📋 رقم الطلب: #{order_id}\n"
        f"📋 رقم الطلب الخاص بالقسم: #{section_id}\n"
        f"📱 الخدمة: {service['service_code']}\n"
        f"📱 اسم الخدمة: {service['name']}\n"
        f"🔢 العدد: {order_data['quantity']}\n"
        f"📱 رقم المحفظة: {order_data['wallet_num']}\n"
        f"🏦 اسم المحفظة: {order_data['wallet_name']}\n"
        f"📞 الرقم: {order_data['target_num']}\n"
        f"💰 المبلغ: {order_data['price']} جنيه"
    )
    markup = developer_order_markup(order_id)
    try:
        bot.send_photo(DEVELOPER_ID, order_data['receipt_file_id'],
                       caption=text, reply_markup=markup, parse_mode='HTML')
    except Exception:
        try:
            bot.send_message(DEVELOPER_ID, text, reply_markup=markup, parse_mode='HTML')
        except Exception:
            pass


# ==================== KEYBOARDS ====================

def main_menu_markup(user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("فودافـون", callback_data="section_vodafone",
            style='primary', icon_custom_emoji_id=E_VODAFONE),
        types.InlineKeyboardButton("وي", callback_data="section_we",
            style='primary', icon_custom_emoji_id=E_WE)
    )
    markup.add(
        types.InlineKeyboardButton("النترا", callback_data="section_natera",
            style='success', icon_custom_emoji_id=E_NATERA),
        types.InlineKeyboardButton("اورنج", callback_data="section_orange",
            style='success', icon_custom_emoji_id=E_ORANGE)
    )
    markup.add(
        types.InlineKeyboardButton("اتـصالات", callback_data="section_etisalat",
            style='danger', icon_custom_emoji_id=E_ETISALAT),
        types.InlineKeyboardButton("تمويـن", callback_data="section_tamween",
            style='danger', icon_custom_emoji_id=E_TAMWEEN)
    )
    markup.add(
        types.InlineKeyboardButton("طلباتي", callback_data="section_orders",
            style='primary', icon_custom_emoji_id=E_ORDERS),
        types.InlineKeyboardButton("الإحالات", callback_data="section_referrals",
            style='primary', icon_custom_emoji_id=E_REFERRAL)
    )
    markup.add(types.InlineKeyboardButton("الدعم الفني", callback_data="section_support",
        style='success', icon_custom_emoji_id=E_SUPPORT))
    if is_admin(user_id):
        markup.add(types.InlineKeyboardButton("⚙️ قسم الادمن", callback_data="section_admin",
            style='danger', icon_custom_emoji_id=EMOJI[6]))
    return markup


def vodafone_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📱 سحب بيانات فودافون", callback_data="service_vodafone_data",
        style='danger', icon_custom_emoji_id=EMOJI[1]))
    markup.add(types.InlineKeyboardButton("💎 بيانات برقم مميز فودافون", callback_data="service_vodafone_vip",
        style='primary', icon_custom_emoji_id=EMOJI[2]))
    markup.add(types.InlineKeyboardButton("🔑 سحب ملكية سابقة 010", callback_data="service_vodafone_ownership",
        style='success', icon_custom_emoji_id=EMOJI[3]))
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_main",
        style='danger', icon_custom_emoji_id=E_BACK))
    return markup


def we_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔑 قسم بطايق وي", callback_data="service_we_cards",
        style='primary', icon_custom_emoji_id=EMOJI[5]))
    markup.add(types.InlineKeyboardButton("🔑 قسم داتا وي", callback_data="service_we_data",
        style='danger', icon_custom_emoji_id=EMOJI[7]))
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_main",
        style='success', icon_custom_emoji_id=E_BACK))
    return markup


def natera_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📱 قسم ارقام نترا", callback_data="service_natera_numbers",
        style='danger', icon_custom_emoji_id=EMOJI[1]))
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_main",
        style='success', icon_custom_emoji_id=E_BACK))
    return markup


def orange_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📱 بيانات اورنج", callback_data="service_orange_data",
        style='danger', icon_custom_emoji_id=EMOJI[1]))
    markup.add(types.InlineKeyboardButton("🔓 فتح كاشات", callback_data="service_orange_open_cache",
        style='primary', icon_custom_emoji_id=E_BACK))
    markup.add(types.InlineKeyboardButton("🔑 قفل كاشات", callback_data="service_orange_close_cache",
        style='danger', icon_custom_emoji_id=EMOJI[6]))
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_main",
        style='success', icon_custom_emoji_id=E_BACK))
    return markup


def etisalat_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📱 بـيـانـات اتـصـالات", callback_data="service_etisalat_data",
        style='primary', icon_custom_emoji_id=EMOJI[1]))
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_main",
        style='success', icon_custom_emoji_id=E_BACK))
    return markup


def orders_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📋 الطلب", callback_data="noop",
            style='primary', icon_custom_emoji_id=EMOJI[8]),
        types.InlineKeyboardButton("📊 الحالة", callback_data="noop",
            style='success', icon_custom_emoji_id=EMOJI[9])
    )
    markup.add(types.InlineKeyboardButton("📭 لا توجد طلبات", callback_data="noop",
        style='danger', icon_custom_emoji_id=EMOJI[10]))
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_main",
        style='success', icon_custom_emoji_id=E_BACK))
    return markup


def support_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📞 وصف مشكلة في السحب", callback_data="support_withdrawal",
        style='danger', icon_custom_emoji_id=EMOJI[14]))
    markup.add(types.InlineKeyboardButton("❓ استفسار عن البوت", callback_data="support_inquiry",
        style='primary', icon_custom_emoji_id=EMOJI[1]))
    markup.add(types.InlineKeyboardButton("🔍 دعم البيانات المشكوك بها", callback_data="support_suspicious",
        style='success', icon_custom_emoji_id=EMOJI[19]))
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_main",
        style='success', icon_custom_emoji_id=E_BACK))
    return markup


def referrals_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_main",
        style='success', icon_custom_emoji_id=E_BACK))
    return markup


def admin_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("➕ اضافه قسم", callback_data="admin_add_section",
            style='success', icon_custom_emoji_id=EMOJI[7]),
        types.InlineKeyboardButton("📂 إداره الاقسام", callback_data="admin_manage_sections",
            style='primary', icon_custom_emoji_id=EMOJI[8])
    )
    markup.add(
        types.InlineKeyboardButton("💰 تغيير رقم الكاش", callback_data="admin_change_cash",
            style='danger', icon_custom_emoji_id=EMOJI[16]),
        types.InlineKeyboardButton("📢 إذاعه للكل", callback_data="admin_broadcast",
            style='success', icon_custom_emoji_id=E_BCAST)
    )
    markup.add(
        types.InlineKeyboardButton("✏️ رساله الترحيب", callback_data="admin_edit_welcome",
            style='primary', icon_custom_emoji_id=EMOJI[2]),
        types.InlineKeyboardButton("🖼 صورة الترحيب", callback_data="admin_edit_image",
            style='success', icon_custom_emoji_id=EMOJI[3])
    )
    markup.add(
        types.InlineKeyboardButton("🔗 قناة الثقة", callback_data="admin_trust_channel",
            style='danger', icon_custom_emoji_id=EMOJI[4]),
        types.InlineKeyboardButton("👤 حساب الدعم", callback_data="admin_support_account",
            style='primary', icon_custom_emoji_id=EMOJI[5])
    )
    markup.add(
        types.InlineKeyboardButton("👥 المستخدمين", callback_data="admin_users",
            style='success', icon_custom_emoji_id=EMOJI[13]),
        types.InlineKeyboardButton("📊 الاحصائيات", callback_data="admin_stats",
            style='primary', icon_custom_emoji_id=E_STATS)
    )
    markup.add(
        types.InlineKeyboardButton("📌 الاشتراك الاجباري", callback_data="admin_subscription",
            style='danger', icon_custom_emoji_id=EMOJI[0]),
        types.InlineKeyboardButton("⏳ الطلبات المعلقة", callback_data="admin_pending",
            style='success', icon_custom_emoji_id=EMOJI[19])
    )
    markup.add(
        types.InlineKeyboardButton("📝 رساله داخل الاقسام", callback_data="admin_edit_section_welcome",
            style='success', icon_custom_emoji_id=EMOJI[18]),
        types.InlineKeyboardButton("📝 رساله داخل الازرار", callback_data="admin_edit_button_welcome",
            style='primary', icon_custom_emoji_id=EMOJI[20])
    )
    markup.add(types.InlineKeyboardButton("🎨 تغيير لون الاقسام والازرار", callback_data="admin_colors",
        style='danger', icon_custom_emoji_id=EMOJI[21]))
    markup.add(types.InlineKeyboardButton("🖼 صور الأقسام", callback_data="admin_section_images",
        style='primary', icon_custom_emoji_id=EMOJI[3]))
    markup.add(types.InlineKeyboardButton("📡 إعداد قناة الثقة", callback_data="admin_setup_trust",
        style='success', icon_custom_emoji_id=EMOJI[4]))
    markup.add(types.InlineKeyboardButton("⏸ إيقاف / تشغيل الأقسام", callback_data="admin_toggle_sections",
        style='danger', icon_custom_emoji_id=EMOJI[9]))
    # ── الميزات الجديدة التسع ──
    markup.add(types.InlineKeyboardButton("━━━━ ادارة المستخدمين ━━━━", callback_data="noop"))
    markup.add(
        types.InlineKeyboardButton("🚫 حظر مستخدم", callback_data="admin_ban",
            style='danger', icon_custom_emoji_id=EMOJI[14]),
        types.InlineKeyboardButton("✅ فك حظر مستخدم", callback_data="admin_unban",
            style='success', icon_custom_emoji_id=EMOJI[0])
    )
    markup.add(
        types.InlineKeyboardButton("📋 قائمة المحظورين", callback_data="admin_banned_list",
            style='primary', icon_custom_emoji_id=EMOJI[1]),
        types.InlineKeyboardButton("📨 رسالة لمستخدم", callback_data="admin_msg_user",
            style='success', icon_custom_emoji_id=EMOJI[5])
    )
    markup.add(
        types.InlineKeyboardButton("🔍 بحث عن مستخدم", callback_data="admin_search_user",
            style='primary', icon_custom_emoji_id=EMOJI[1])
    )
    markup.add(types.InlineKeyboardButton("━━━━ ادارة الخدمات ━━━━", callback_data="noop"))
    markup.add(
        types.InlineKeyboardButton("💲 تغيير سعر خدمة", callback_data="admin_change_price",
            style='danger', icon_custom_emoji_id=EMOJI[16]),
        types.InlineKeyboardButton("✅ الطلبات المقبولة", callback_data="admin_accepted_orders",
            style='success', icon_custom_emoji_id=EMOJI[19])
    )
    markup.add(
        types.InlineKeyboardButton("🔎 عرض طلب بالرقم", callback_data="admin_view_order",
            style='primary', icon_custom_emoji_id=EMOJI[1])
    )
    markup.add(types.InlineKeyboardButton("━━━━ ادارة الادمن ━━━━", callback_data="noop"))
    markup.add(
        types.InlineKeyboardButton("🛡 ادمن بوت كامل", callback_data="admin_admins",
            style='primary', icon_custom_emoji_id=EMOJI[11]),
        types.InlineKeyboardButton("🗂 ادمن قسم معين", callback_data="admin_section_admin",
            style='success', icon_custom_emoji_id=EMOJI[8])
    )
    markup.add(types.InlineKeyboardButton("✨ إيموجي مميزة للنصوص", callback_data="admin_emoji_guide",
        style='primary', icon_custom_emoji_id=EMOJI[21]))
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_main",
        style='success', icon_custom_emoji_id=E_BACK))
    return markup


def confirm_order_markup(service_key, remaining=120):
    mins = remaining // 60
    secs = remaining % 60
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"⏱ {mins:02d}:{secs:02d}", callback_data="noop"))
    markup.add(
        types.InlineKeyboardButton("✅ تأكيد", callback_data=f"confirm_order_{service_key}",
            style='success', icon_custom_emoji_id=E_CONFIRM),
        types.InlineKeyboardButton("❌ رفض الطلب", callback_data="cancel_order",
            style='danger', icon_custom_emoji_id=E_CANCEL)
    )
    return markup


def developer_order_markup(order_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ قبول", callback_data=f"dev_accept_{order_id}",
            style='success', icon_custom_emoji_id=E_CONFIRM),
        types.InlineKeyboardButton("❌ رفض", callback_data=f"dev_reject_{order_id}",
            style='danger', icon_custom_emoji_id=E_CANCEL)
    )
    markup.add(types.InlineKeyboardButton("💬 إرسال رسالة", callback_data=f"dev_reply_{order_id}",
        style='primary', icon_custom_emoji_id=EMOJI[5]))
    return markup


def developer_ticket_markup(ticket_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💬 رد على التذكرة", callback_data=f"dev_ticket_reply_{ticket_id}",
        style='primary', icon_custom_emoji_id=EMOJI[5]))
    return markup


def subscription_markup(not_subscribed):
    markup = types.InlineKeyboardMarkup()
    for sub in not_subscribed:
        if sub['sub_type'] == 'telegram':
            cid = sub['channel_id']
            url = f"https://t.me/{cid.lstrip('@')}"
            markup.add(types.InlineKeyboardButton(f"اشترك هنا ✨ | {sub['channel_name']}", url=url,
                style='danger', icon_custom_emoji_id=EMOJI[4]))
        else:
            markup.add(types.InlineKeyboardButton(f"اشترك هنا ✨ | {sub['channel_name']}", url=sub['channel_id'],
                style='danger', icon_custom_emoji_id=EMOJI[4]))
    markup.add(types.InlineKeyboardButton("تحقق من الاشتراك ✅", callback_data="check_subscription",
        style='success', icon_custom_emoji_id=EMOJI[0]))
    return markup


# ==================== SEND MAIN MENU ====================

def send_main_menu(chat_id, user_id):
    name = f'<a href="tg://user?id={user_id}">العميل</a>'
    welcome_text = get_setting('welcome_text', '').replace('{name}', name)
    welcome_image = get_setting('welcome_image', 'https://b.top4top.io/p_3791mznyg0.jpg')
    markup = main_menu_markup(user_id)
    try:
        bot.send_photo(chat_id, welcome_image, caption=welcome_text,
                       reply_markup=markup, parse_mode='HTML')
    except Exception:
        bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode='HTML')


STOP_IMAGE_URL = 'https://j.top4top.io/p_3793scp9c0.png'

SECTION_NAMES_AR = {
    'vodafone': 'فودافون',
    'we':       'وي',
    'natera':   'النترا',
    'orange':   'اورنج',
    'etisalat': 'اتصالات',
    'tamween':  'تموين',
}


def is_section_disabled(section_key: str) -> bool:
    return get_setting(f'section_disabled_{section_key}', '0') == '1'


def send_section_with_image(chat_id, msg_id, section_key, text, markup):
    """إرسال قسم مع صورته المخصصة. يحذف الرسالة القديمة وينشئ رسالة جديدة مع الصورة."""
    # ── فحص: هل القسم موقوف؟ ──
    if is_section_disabled(section_key):
        back_m = types.InlineKeyboardMarkup()
        back_m.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_main",
            style='success', icon_custom_emoji_id=E_BACK))
        try:
            bot.delete_message(chat_id, msg_id)
        except Exception:
            pass
        try:
            bot.send_photo(
                chat_id, STOP_IMAGE_URL,
                caption=(
                    f"🛡️ قسم {SECTION_NAMES_AR.get(section_key, section_key)} متوقف مؤقتاً\n\n"
                    "سيعود قريباً إن شاء الله 🔄"
                ),
                reply_markup=back_m, parse_mode='HTML'
            )
        except Exception:
            bot.send_message(
                chat_id,
                f"🛡️ قسم {SECTION_NAMES_AR.get(section_key, section_key)} متوقف مؤقتاً\n\nسيعود قريباً 🔄",
                reply_markup=back_m, parse_mode='HTML'
            )
        return

    img = get_section_image(section_key)
    try:
        bot.delete_message(chat_id, msg_id)
    except Exception:
        pass
    try:
        bot.send_photo(chat_id, img, caption=text, reply_markup=markup, parse_mode='HTML')
    except Exception:
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode='HTML')


def send_subscription_screen(chat_id, user_id, not_subscribed):
    set_state(user_id, 'awaiting_subscription')
    text = (
        "👑 تنبيه الاشتراك الإجباري 👑\n\n"
        "عذراً عزيزي المستخدم، لضمان استمرارية الخدمة المجانية وتلقي التحديثات، "
        "يجب عليك الانضمام إلى قنواتنا الرسمية أولاً:\n\n"
        "✨ بعد الانضمام اضغط على زر التحقق بالأسفل."
    )
    markup = subscription_markup(not_subscribed)
    bot.send_message(chat_id, text, reply_markup=markup)


# ==================== SERVICE FLOW ====================

def start_service_flow(chat_id, user_id, service_key):
    service = dict(SERVICES[service_key])
    # Use dynamic price if admin changed it
    dynamic_price = get_service_price(service_key)
    service['price'] = dynamic_price
    transfer_num = get_transfer_num(service['section'])
    custom_welcome = get_setting(f'service_welcome_{service_key}', '')
    set_state(user_id, 'await_quantity', service_key=service_key, service=service)

    if custom_welcome:
        text = custom_welcome
    else:
        text = (
            f"انـت الان داخـل قـسـم : {service['emoji']} {service['name']}\n"
            f"سـعـر الـخـدمـة لـكـل {service['quantity_label']} : {dynamic_price} 💰\n"
            f"رقـم الـتـحويـل : {transfer_num} 💳\n\n"
            f"🎯 كم {service['quantity_label']} تريد تطبيق الخدمة عليه؟\n"
            f"✏️ أرسل العدد المطلوب (أرقام فقط):"
        )
    bot.send_message(chat_id, text)


# ==================== CAPTCHA ====================

def send_captcha(chat_id, user_id):
    a = random.randint(1, 20)
    b = random.randint(5, 30)
    answer = a + b
    captcha_data[user_id] = {'answer': answer, 'attempts': 0}
    set_state(user_id, 'captcha')
    bot.send_message(
        chat_id,
        f"👑 مرحباً بك في بوت L • V 👑\n\n"
        f"✅ للتحقق من هويتك وحماية البوت من الروبوتات\n\n"
        f"📱 يرجى حل هذه المسأله\n\n"
        f"<b>{a} + {b} = ؟؟</b>",
        parse_mode='HTML'
    )


# ==================== MAIN MESSAGE HANDLER ====================

@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'audio', 'voice'])
def handle_all_messages(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text or message.caption or ''

    # Handle /start command
    if message.content_type == 'text' and text.startswith('/start'):
        if check_user_banned(user_id):
            bot.send_message(chat_id, "❌ أنت محظور من استخدام هذا البوت.")
            return

        username = message.from_user.username
        first_name = message.from_user.first_name or ''
        referred_by = None
        parts = text.split()
        if len(parts) > 1:
            try:
                ref_id = int(parts[1])
                if ref_id != user_id:
                    referred_by = ref_id
            except Exception:
                pass

        is_new = add_user(user_id, username, first_name, referred_by)

        if is_new:
            try:
                bot.send_message(
                    DEVELOPER_ID,
                    f"تم دخول شخص جديد الي بوت سحب بيانات ✨\n\n"
                    f"اليوزر : @{username or 'بدون'}\n"
                    f"الايدي : {user_id}"
                )
            except Exception:
                pass
            if referred_by:
                try:
                    bot.send_message(
                        referred_by,
                        f"تم دخول شخص عبر الرابط الخاص بك ✨\n\n"
                        f"اليوزر : @{username or 'بدون'}\n"
                        f"الايدي : {user_id}"
                    )
                except Exception:
                    pass

        cancel_countdown(user_id)
        clear_state(user_id)
        # Skip captcha if user already passed it before
        if has_passed_captcha(user_id) or is_admin(user_id):
            is_ok, not_subscribed = check_subscription(user_id)
            if not is_ok:
                send_subscription_screen(chat_id, user_id, not_subscribed)
            else:
                send_main_menu(chat_id, user_id)
        else:
            send_captcha(chat_id, user_id)
        return

    # Check ban
    if check_user_banned(user_id) and not is_admin(user_id):
        bot.send_message(chat_id, "❌ أنت محظور من استخدام هذا البوت.")
        return

    state = get_state(user_id)

    # ==================== CAPTCHA STATE ====================
    if state == 'captcha':
        if user_id not in captcha_data:
            send_captcha(chat_id, user_id)
            return
        if message.content_type != 'text':
            bot.send_message(chat_id, "❌ أرسل رقماً صحيحاً فقط.")
            return
        try:
            answer = int(text.strip())
        except Exception:
            captcha_data[user_id]['attempts'] += 1
            remaining = 3 - captcha_data[user_id]['attempts']
            if remaining <= 0:
                _ban_user(chat_id, user_id)
                return
            bot.send_message(chat_id, f"❌ إجابة خاطئة! المحاولات المتبقية: {remaining}")
            return

        if answer == captcha_data[user_id]['answer']:
            captcha_data.pop(user_id, None)
            clear_state(user_id)
            mark_captcha_passed(user_id)
            is_ok, not_subscribed = check_subscription(user_id)
            if not is_ok:
                send_subscription_screen(chat_id, user_id, not_subscribed)
            else:
                send_main_menu(chat_id, user_id)
        else:
            captcha_data[user_id]['attempts'] += 1
            remaining = 3 - captcha_data[user_id]['attempts']
            if remaining <= 0:
                _ban_user(chat_id, user_id)
                return
            bot.send_message(chat_id, f"❌ إجابة خاطئة! المحاولات المتبقية: {remaining}")
        return

    # ==================== SERVICE FLOW STATES ====================

    if state == 'await_quantity':
        if message.content_type != 'text':
            bot.send_message(chat_id, "❌ يرجى إرسال رقم صحيح أكبر من صفر فقط")
            return
        try:
            quantity = int(text.strip())
            if quantity <= 0:
                raise ValueError
        except Exception:
            bot.send_message(chat_id, "❌ يرجى إرسال رقم صحيح أكبر من صفر فقط")
            return
        service = get_data(user_id, 'service')
        price = round(service['price'] * quantity, 2)
        set_state(user_id, 'await_receipt', quantity=quantity, price=price)
        bot.send_message(
            chat_id,
            f"✅ تم تحديد عدد الأرقام: {quantity}\n"
            f"💰 السعر الإجمالي: {price} جنيه\n\n"
            f"📤 أرسل صورة إيصال التحويل الآن:"
        )
        return

    if state == 'await_receipt':
        if message.content_type != 'photo':
            bot.send_message(chat_id, "❌ يرجى إرسال صورة إيصال التحويل")
            return
        file_id = message.photo[-1].file_id
        set_state(user_id, 'await_wallet_num', receipt_file_id=file_id)
        bot.send_message(
            chat_id,
            "✅ تم استلام الإيصال!\n\n"
            "📱 أرسل رقم المحفظة التي تم التحويل منها الآن:"
        )
        return

    if state == 'await_wallet_num':
        if message.content_type != 'text':
            bot.send_message(chat_id, "❌ يرجى إرسال رقم المحفظة")
            return
        set_state(user_id, 'await_wallet_name', wallet_num=text.strip())
        bot.send_message(chat_id, "✅ تم استلام رقم المحفظة!\n\n🏦 أرسل اسم المحفظة الآن:")
        return

    if state == 'await_wallet_name':
        if message.content_type != 'text':
            bot.send_message(chat_id, "❌ يرجى إرسال اسم المحفظة")
            return
        service = get_data(user_id, 'service')
        set_state(user_id, 'await_target', wallet_name=text.strip())
        bot.send_message(chat_id, f"✅ تم استلام اسم المحفظة!\n\n{service['target_prompt']}")
        return

    if state == 'await_target':
        if message.content_type != 'text':
            bot.send_message(chat_id, "❌ يرجى إرسال الرقم المطلوب")
            return
        target_num = text.strip()
        service_key = get_data(user_id, 'service_key')
        service = get_data(user_id, 'service')
        quantity = get_data(user_id, 'quantity')
        price = get_data(user_id, 'price')
        wallet_num = get_data(user_id, 'wallet_num')
        wallet_name = get_data(user_id, 'wallet_name')
        receipt_file_id = get_data(user_id, 'receipt_file_id')

        order_id, section_id = save_order(
            user_id, service_key, service['name'], service['service_code'],
            quantity, price, wallet_num, wallet_name, target_num, receipt_file_id
        )

        summary_text = (
            f"📋 ملخص الطلب:\n\n"
            f"📱 الخدمة: {service['name']}\n"
            f"📱 رقم المحفظة: {wallet_num}\n"
            f"🏦 اسم المحفظة: {wallet_name}\n"
            f"📞 الرقم: {target_num}\n"
            f"💰 المبلغ: {price} جنيه\n\n"
            f"⏳ لديك دقيقتين لمراجعة البيانات والتأكد من صحتها\n"
            f"💎 اضغط تأكيد لإرسال الطلب أو إلغاء للخروج"
        )
        markup = confirm_order_markup(service_key, 120)
        has_photo = True
        try:
            sent = bot.send_photo(chat_id, receipt_file_id,
                                  caption=summary_text, reply_markup=markup)
        except Exception:
            has_photo = False
            sent = bot.send_message(chat_id, summary_text, reply_markup=markup)

        order_data = {
            'service_key': service_key,
            'service': service,
            'quantity': quantity,
            'price': price,
            'wallet_num': wallet_num,
            'wallet_name': wallet_name,
            'target_num': target_num,
            'receipt_file_id': receipt_file_id,
            'order_id': order_id,
            'section_id': section_id,
        }
        set_state(user_id, 'await_confirm',
                  confirm_msg_id=sent.message_id,
                  has_photo=has_photo,
                  target_num=target_num,
                  order_id=order_id,
                  section_id=section_id,
                  order_data=order_data)
        start_countdown(chat_id, user_id, sent.message_id, has_photo, order_data)
        return

    # ==================== SUPPORT STATE ====================

    if state == 'support_message':
        ticket_type = get_data(user_id, 'ticket_type')
        support_photos = get_data(user_id, 'support_photos') or []

        if message.content_type == 'text' and text.strip() == 'تم':
            support_text = get_data(user_id, 'support_text') or ''
            conn = get_db()
            c = conn.cursor()
            c.execute('INSERT INTO tickets (user_id, ticket_type, message) VALUES (?, ?, ?)',
                      (user_id, ticket_type, support_text))
            ticket_id = c.lastrowid
            for ph in support_photos:
                c.execute('INSERT INTO ticket_photos (ticket_id, file_id) VALUES (?, ?)', (ticket_id, ph))
            conn.commit()
            conn.close()

            bot.send_message(
                chat_id,
                f"✅ تم إرسال التذكرة بنجاح!\n\n"
                f"📋 رقم التذكرة: #{ticket_id}\n"
                f"📌 النوع: {ticket_type}\n\n"
                f"✨ سيتم الرد عليك في أقرب وقت"
            )

            dev_text = (
                f"🎫 <b>تذكرة جديدة #{ticket_id}</b>\n\n"
                f"👤 المستخدم: <a href='tg://user?id={user_id}'>{user_id}</a>\n"
                f"📌 النوع: {ticket_type}\n"
                f"💬 الرسالة:\n{support_text}"
            )
            t_markup = developer_ticket_markup(ticket_id)
            try:
                if support_photos:
                    bot.send_photo(DEVELOPER_ID, support_photos[0],
                                   caption=dev_text, reply_markup=t_markup, parse_mode='HTML')
                    for ph in support_photos[1:]:
                        bot.send_photo(DEVELOPER_ID, ph)
                else:
                    bot.send_message(DEVELOPER_ID, dev_text, reply_markup=t_markup, parse_mode='HTML')
            except Exception:
                pass

            clear_state(user_id)
            send_main_menu(chat_id, user_id)

        elif message.content_type == 'photo':
            file_id = message.photo[-1].file_id
            support_photos.append(file_id)
            set_state(user_id, 'support_message', support_photos=support_photos)
            bot.send_message(chat_id, "✅ تم إرسال التذكرة بنجاح!\n\n"
                                      f"📋 رقم التذكرة: #\n"
                                      f"📌 النوع: {ticket_type}\n\n"
                                      f"✨ سيتم الرد عليك في أقرب وقت")
            # Actually for photos, just confirm and wait for تم
            # Re-set the message
            bot.send_message(chat_id, "📝 تم حفظ الصورة. أرسل صوراً أخرى أو اكتب \"تم\" للإنهاء")

        elif message.content_type == 'text':
            current = get_data(user_id, 'support_text') or ''
            new_text = (current + '\n' + text).strip()
            set_state(user_id, 'support_message', support_text=new_text)
            bot.send_message(chat_id, "📝 تم حفظ الرسالة. أرسل صوراً أو اكتب \"تم\" للإنهاء")
        return

    # ==================== ADMIN STATES ====================

    if not is_admin(user_id):
        return

    if state == 'admin_broadcast':
        conn = get_db()
        users = conn.execute('SELECT user_id FROM users').fetchall()
        conn.close()
        success = 0
        for u in users:
            try:
                if message.content_type == 'text':
                    bot.send_message(u['user_id'],
                                     f"📢 إذاعه من الادمن\n\n{text}")
                elif message.content_type == 'photo':
                    bot.send_photo(u['user_id'], message.photo[-1].file_id,
                                   caption=f"📢 إذاعه من الادمن\n\n{message.caption or ''}")
                elif message.content_type == 'video':
                    bot.send_video(u['user_id'], message.video.file_id,
                                   caption=f"📢 إذاعه من الادمن\n\n{message.caption or ''}")
                success += 1
                time.sleep(0.04)
            except Exception:
                pass
        bot.send_message(chat_id, f"✅ تم إرسال الإذاعة لـ {success} مستخدم")
        clear_state(user_id)
        return

    if state == 'admin_edit_welcome':
        if message.content_type == 'text':
            set_setting('welcome_text', text)
            bot.send_message(chat_id, "✅ تم تحديث رسالة الترحيب بنجاح!")
        clear_state(user_id)
        return

    if state == 'admin_edit_image':
        if message.content_type == 'text':
            set_setting('welcome_image', text.strip())
            bot.send_message(chat_id, "✅ تم تحديث صورة الترحيب بنجاح!")
        clear_state(user_id)
        return

    if state == 'admin_trust_channel':
        if message.content_type == 'text':
            channel_id = text.strip()
            set_setting('trust_channel_id', channel_id)
            current = get_setting('trust_channel_id', '')
            bot.send_message(chat_id,
                f"✅ تم حفظ قناة الثقة بنجاح!\n"
                f"📡 الـ ID: <code>{current}</code>\n\n"
                f"⚠️ تأكد أن البوت أدمن في القناة حتى تعمل ميزة النشر التلقائي.",
                parse_mode='HTML')
        clear_state(user_id)
        return

    if state == 'admin_set_section_image':
        if message.content_type == 'text':
            section_key = get_data(user_id, 'section_image_key')
            image_url = text.strip()
            set_setting(f'image_{section_key}', image_url)
            section_names = {
                'vodafone': 'فودافون', 'we': 'وي', 'natera': 'النترا',
                'orange': 'اورنج', 'etisalat': 'اتصالات', 'tamween': 'تموين',
                'main': 'الرئيسية / الترحيب'
            }
            sname = section_names.get(section_key, section_key)
            bot.send_message(chat_id, f"✅ تم تحديث صورة قسم {sname} بنجاح!")
        clear_state(user_id)
        return

    if state == 'admin_support_account':
        if message.content_type == 'text':
            set_setting('support_username', text.strip())
            bot.send_message(chat_id, "✅ تم حفظ حساب الدعم الفني بنجاح!")
        clear_state(user_id)
        return

    if state == 'admin_add_sub_telegram':
        if message.content_type == 'text':
            channel = text.strip()
            if not channel.startswith('@'):
                channel = '@' + channel
            try:
                chat_info = bot.get_chat(channel)
                name = chat_info.title or channel
            except Exception:
                name = channel
            conn = get_db()
            conn.execute('INSERT INTO subscriptions (channel_id, channel_name, sub_type) VALUES (?, ?, ?)',
                         (channel, name, 'telegram'))
            conn.commit()
            conn.close()
            bot.send_message(chat_id, f"✅ تم إضافة قناة {name} للاشتراك الإجباري!")
        clear_state(user_id)
        return

    if state == 'admin_add_sub_link':
        if message.content_type == 'text':
            url = text.strip()
            conn = get_db()
            conn.execute('INSERT INTO subscriptions (channel_id, channel_name, sub_type) VALUES (?, ?, ?)',
                         (url, 'اشترك هنا', 'url'))
            conn.commit()
            conn.close()
            bot.send_message(chat_id, "✅ تم إضافة الرابط للاشتراك الإجباري!")
        clear_state(user_id)
        return

    if state == 'admin_add_admin':
        if message.content_type == 'text':
            identifier = text.strip().lstrip('@')
            try:
                if identifier.isdigit():
                    new_uid = int(identifier)
                    uname = identifier
                else:
                    info = bot.get_chat(f'@{identifier}')
                    new_uid = info.id
                    uname = identifier
                conn = get_db()
                conn.execute('INSERT OR REPLACE INTO admins (user_id, username) VALUES (?, ?)', (new_uid, uname))
                conn.commit()
                conn.close()
                bot.send_message(chat_id, f"✅ تم إضافة المشرف {uname} بنجاح!")
            except Exception as e:
                bot.send_message(chat_id, f"❌ خطأ: {e}")
        clear_state(user_id)
        return

    if state == 'admin_add_section_name':
        if message.content_type == 'text':
            section_name = text.strip()
            set_state(user_id, 'admin_add_section_pos', new_section_name=section_name)
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton("⬆️ فوق الأزرار التالية", callback_data="admin_sec_pos_above"),
                types.InlineKeyboardButton("⬇️ تحت الأزرار التالية", callback_data="admin_sec_pos_below")
            )
            bot.send_message(chat_id, f"📍 أين تريد إضافة قسم '{section_name}'؟", reply_markup=markup)
        return

    if state == 'admin_add_section_welcome':
        if message.content_type == 'text':
            section_name = get_data(user_id, 'new_section_name')
            position = get_data(user_id, 'section_position', 'after')
            welcome_text_val = text.strip() if text.strip() != '-' else ''
            conn = get_db()
            conn.execute('INSERT INTO dynamic_sections (section_name, welcome_text, position) VALUES (?, ?, ?)',
                         (section_name, welcome_text_val, position))
            conn.commit()
            conn.close()
            bot.send_message(chat_id, f"✅ تم إضافة قسم '{section_name}' بنجاح!")
            clear_state(user_id)
        return

    if state == 'admin_edit_sec_welcome':
        if message.content_type == 'text':
            section = get_data(user_id, 'editing_section')
            set_setting(f'section_welcome_{section}', text)
            bot.send_message(chat_id, f"✅ تم تحديث رسالة ترحيب قسم {section}!")
        clear_state(user_id)
        return

    if state == 'admin_edit_btn_welcome':
        if message.content_type == 'text':
            skey = get_data(user_id, 'editing_service')
            set_setting(f'service_welcome_{skey}', text)
            bot.send_message(chat_id, f"✅ تم تحديث رسالة ترحيب الخدمة!")
        clear_state(user_id)
        return

    if state == 'admin_change_cash':
        if message.content_type == 'text':
            section = get_data(user_id, 'cash_section')
            new_num = text.strip()
            set_setting(f'cash_{section}', new_num)
            bot.send_message(chat_id, f"✅ تم تحديث رقم الكاش لقسم {section} إلى {new_num}")
        clear_state(user_id)
        return

    # ── ميزة 1: حظر مستخدم بالـ ID ──
    if state == 'admin_ban_id':
        if message.content_type == 'text':
            try:
                target = int(text.strip())
                conn = get_db()
                conn.execute('UPDATE users SET is_banned = 1 WHERE user_id = ?', (target,))
                conn.commit()
                conn.close()
                bot.send_message(chat_id, f"✅ تم حظر المستخدم {target} بنجاح!")
                try:
                    bot.send_message(target, "🚫 تم حظرك من استخدام هذا البوت.")
                except Exception:
                    pass
            except Exception:
                bot.send_message(chat_id, "❌ يرجى إرسال ID رقمي صحيح.")
        clear_state(user_id)
        return

    # ── ميزة 2: فك حظر مستخدم بالـ ID ──
    if state == 'admin_unban_id':
        if message.content_type == 'text':
            try:
                target = int(text.strip())
                conn = get_db()
                conn.execute('UPDATE users SET is_banned = 0 WHERE user_id = ?', (target,))
                conn.commit()
                conn.close()
                bot.send_message(chat_id, f"✅ تم فك حظر المستخدم {target} بنجاح!")
                try:
                    bot.send_message(target, "✅ تم رفع الحظر عنك، يمكنك استخدام البوت الآن.")
                except Exception:
                    pass
            except Exception:
                bot.send_message(chat_id, "❌ يرجى إرسال ID رقمي صحيح.")
        clear_state(user_id)
        return

    # ── ميزة 4: إرسال رسالة لمستخدم معين ──
    if state == 'admin_msg_user_id':
        if message.content_type == 'text':
            try:
                target = int(text.strip())
                set_state(user_id, 'admin_msg_user_text', msg_target_id=target)
                bot.send_message(chat_id, f"✏️ أرسل الرسالة التي تريد إيصالها للمستخدم {target}:")
            except Exception:
                bot.send_message(chat_id, "❌ يرجى إرسال ID رقمي صحيح.")
                clear_state(user_id)
        return

    if state == 'admin_msg_user_text':
        target = get_data(user_id, 'msg_target_id')
        if target:
            try:
                if message.content_type == 'text':
                    bot.send_message(target, f"📨 رسالة من الإدارة:\n\n{text}")
                elif message.content_type == 'photo':
                    bot.send_photo(target, message.photo[-1].file_id,
                                   caption=f"📨 رسالة من الإدارة:\n\n{message.caption or ''}")
                elif message.content_type == 'video':
                    bot.send_video(target, message.video.file_id,
                                   caption=f"📨 رسالة من الإدارة:\n\n{message.caption or ''}")
                bot.send_message(chat_id, f"✅ تم إرسال الرسالة للمستخدم {target}.")
            except Exception as e:
                bot.send_message(chat_id, f"❌ فشل الإرسال: {e}")
        clear_state(user_id)
        return

    # ── ميزة 5: بحث عن مستخدم بالـ ID ──
    if state == 'admin_search_user_id':
        if message.content_type == 'text':
            try:
                target = int(text.strip())
                row, orders_cnt = get_user_info(target)
                if row:
                    ref_cnt = get_referral_count(target)
                    info = (
                        f"🔍 <b>بيانات المستخدم</b>\n\n"
                        f"👤 الاسم: {row['first_name']}\n"
                        f"🆔 الـ ID: <code>{row['user_id']}</code>\n"
                        f"🔗 اليوزر: @{row['username'] or 'بدون'}\n"
                        f"📅 تاريخ الانضمام: {row['joined_at']}\n"
                        f"📦 عدد الطلبات: {orders_cnt}\n"
                        f"👥 الإحالات: {ref_cnt}\n"
                        f"🚫 محظور: {'نعم' if row['is_banned'] else 'لا'}\n"
                        f"✅ تجاوز الكابتشا: {'نعم' if row['captcha_passed'] else 'لا'}"
                    )
                    markup = types.InlineKeyboardMarkup()
                    if row['is_banned']:
                        markup.add(types.InlineKeyboardButton(
                            "✅ فك الحظر", callback_data=f"admin_quick_unban_{target}", style='success'))
                    else:
                        markup.add(types.InlineKeyboardButton(
                            "🚫 حظر", callback_data=f"admin_quick_ban_{target}", style='danger'))
                    markup.add(types.InlineKeyboardButton(
                        "📨 إرسال رسالة", callback_data=f"admin_quick_msg_{target}", style='primary'))
                    bot.send_message(chat_id, info, reply_markup=markup, parse_mode='HTML')
                else:
                    bot.send_message(chat_id, "❌ المستخدم غير مسجل في قاعدة البيانات.")
            except Exception:
                bot.send_message(chat_id, "❌ يرجى إرسال ID رقمي صحيح.")
        clear_state(user_id)
        return

    # ── ميزة 6: تغيير سعر خدمة ──
    if state == 'admin_change_price_val':
        if message.content_type == 'text':
            skey = get_data(user_id, 'price_service_key')
            try:
                new_price = float(text.strip())
                conn = get_db()
                conn.execute('INSERT OR REPLACE INTO service_prices (service_key, price) VALUES (?, ?)',
                             (skey, new_price))
                conn.commit()
                conn.close()
                svc_name = SERVICES.get(skey, {}).get('name', skey)
                bot.send_message(chat_id, f"✅ تم تغيير سعر خدمة {svc_name} إلى {new_price} جنيه")
            except Exception:
                bot.send_message(chat_id, "❌ يرجى إرسال رقم صحيح.")
        clear_state(user_id)
        return

    # ── ميزة 7: إضافة ادمن قسم معين ──
    if state == 'admin_add_section_admin_id':
        if message.content_type == 'text':
            section = get_data(user_id, 'sec_admin_section')
            try:
                target = int(text.strip())
                conn = get_db()
                conn.execute('INSERT OR IGNORE INTO section_admins (user_id, username, section) VALUES (?, ?, ?)',
                             (target, str(target), section))
                conn.commit()
                conn.close()
                section_names = {
                    'vodafone': 'فودافون', 'we': 'وي', 'natera': 'النترا',
                    'orange': 'اورنج', 'etisalat': 'اتصالات', 'tamween': 'تموين'
                }
                bot.send_message(chat_id,
                    f"✅ تم إضافة المستخدم {target} كادمن لقسم {section_names.get(section, section)}!")
                try:
                    bot.send_message(target,
                        f"🎉 تهانينا! تم تعيينك كادمن لقسم {section_names.get(section, section)}.")
                except Exception:
                    pass
            except Exception:
                bot.send_message(chat_id, "❌ يرجى إرسال ID رقمي صحيح.")
        clear_state(user_id)
        return

    # ── ميزة 9: عرض طلب بالرقم ──
    if state == 'admin_view_order_id':
        if message.content_type == 'text':
            try:
                oid = int(text.strip())
                conn = get_db()
                row = conn.execute('SELECT * FROM orders WHERE id = ?', (oid,)).fetchone()
                conn.close()
                if row:
                    status_map = {'pending': '⏳ معلق', 'accepted': '✅ مقبول', 'rejected': '❌ مرفوض'}
                    info = (
                        f"📦 <b>تفاصيل الطلب #{oid}</b>\n\n"
                        f"👤 المستخدم: <code>{row['user_id']}</code>\n"
                        f"🏷 الخدمة: {row['service_name']}\n"
                        f"📝 الكود: {row['service_code']}\n"
                        f"🔢 الكمية: {row['quantity']}\n"
                        f"💰 السعر: {row['price']} جنيه\n"
                        f"📱 محفظة من: {row['wallet_num']}\n"
                        f"👤 اسم المحفظة: {row['wallet_name']}\n"
                        f"🎯 الرقم المستهدف: {row['target_num']}\n"
                        f"📌 الحالة: {status_map.get(row['status'], row['status'])}\n"
                        f"📅 التاريخ: {row['created_at']}"
                    )
                    markup = types.InlineKeyboardMarkup()
                    if row['status'] == 'pending':
                        markup.add(
                            types.InlineKeyboardButton("✅ قبول", callback_data=f"dev_accept_{oid}",
                                style='success'),
                            types.InlineKeyboardButton("❌ رفض", callback_data=f"dev_reject_{oid}",
                                style='danger')
                        )
                    markup.add(types.InlineKeyboardButton(
                        "📤 عرض الإيصال", callback_data=f"admin_show_receipt_{oid}", style='primary'))
                    bot.send_message(chat_id, info, reply_markup=markup, parse_mode='HTML')
                else:
                    bot.send_message(chat_id, "❌ لا يوجد طلب بهذا الرقم.")
            except Exception:
                bot.send_message(chat_id, "❌ يرجى إرسال رقم طلب صحيح.")
        clear_state(user_id)
        return

    if state == 'admin_reply_order':
        order_id = get_data(user_id, 'reply_order_id')
        conn = get_db()
        row = conn.execute('SELECT user_id FROM orders WHERE id = ?', (order_id,)).fetchone()
        conn.close()
        if row:
            target_uid = row['user_id']
            try:
                if message.content_type == 'text':
                    bot.send_message(target_uid, f"💬 رد من الإدارة على طلبك #{order_id}:\n\n{text}")
                elif message.content_type == 'photo':
                    bot.send_photo(target_uid, message.photo[-1].file_id,
                                   caption=f"💬 رد من الإدارة على طلبك #{order_id}:\n\n{message.caption or ''}")
                elif message.content_type == 'video':
                    bot.send_video(target_uid, message.video.file_id,
                                   caption=f"💬 رد من الإدارة على طلبك #{order_id}:\n\n{message.caption or ''}")
                bot.send_message(chat_id, "✅ تم إرسال الرد للمستخدم.")
            except Exception as e:
                bot.send_message(chat_id, f"❌ خطأ: {e}")
        clear_state(user_id)
        return

    if state == 'admin_reply_ticket':
        ticket_id = get_data(user_id, 'reply_ticket_id')
        conn = get_db()
        row = conn.execute('SELECT user_id FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
        conn.close()
        if row:
            target_uid = row['user_id']
            try:
                if message.content_type == 'text':
                    bot.send_message(target_uid, f"💬 رد من الإدارة على تذكرتك #{ticket_id}:\n\n{text}")
                elif message.content_type == 'photo':
                    bot.send_photo(target_uid, message.photo[-1].file_id,
                                   caption=f"💬 رد من الإدارة على تذكرتك #{ticket_id}:\n\n{message.caption or ''}")
                elif message.content_type == 'video':
                    bot.send_video(target_uid, message.video.file_id,
                                   caption=f"💬 رد من الإدارة على تذكرتك #{ticket_id}:\n\n{message.caption or ''}")
                bot.send_message(chat_id, "✅ تم إرسال الرد.")
            except Exception as e:
                bot.send_message(chat_id, f"❌ خطأ: {e}")
        clear_state(user_id)
        return


def _ban_user(chat_id, user_id):
    conn = get_db()
    conn.execute('UPDATE users SET is_banned = 1 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    captcha_data.pop(user_id, None)
    clear_state(user_id)
    bot.send_message(chat_id, "❌ تم حظرك من البوت بسبب الإجابات الخاطئة المتكررة.")


# ==================== CALLBACK HANDLER ====================

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    data = call.data

    if check_user_banned(user_id) and not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ أنت محظور!", show_alert=True)
        return

    bot.answer_callback_query(call.id)

    # No-op buttons
    if data == 'noop':
        return

    # ==================== SUBSCRIPTION CHECK ====================
    if data == 'check_subscription':
        is_ok, not_subscribed = check_subscription(user_id)
        if is_ok:
            clear_state(user_id)
            try:
                bot.delete_message(chat_id, msg_id)
            except Exception:
                pass
            send_main_menu(chat_id, user_id)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات!", show_alert=True)
            try:
                bot.edit_message_reply_markup(chat_id, msg_id,
                                              reply_markup=subscription_markup(not_subscribed))
            except Exception:
                pass
        return

    # ==================== BACK TO MAIN ====================
    if data == 'back_main':
        cancel_countdown(user_id)
        clear_state(user_id)
        try:
            bot.delete_message(chat_id, msg_id)
        except Exception:
            pass
        send_main_menu(chat_id, user_id)
        return

    # ==================== SECTION NAVIGATION ====================
    def try_edit_caption(new_caption, new_markup):
        try:
            bot.edit_message_caption(chat_id, msg_id, caption=new_caption, reply_markup=new_markup)
        except Exception:
            try:
                bot.edit_message_text(new_caption, chat_id, msg_id, reply_markup=new_markup)
            except Exception:
                bot.send_message(chat_id, new_caption, reply_markup=new_markup)

    if data == 'section_vodafone':
        custom = get_setting('section_welcome_vodafone', '')
        text_out = custom if custom else "📱 قسم فودافون\n\n✨ اختر القسم المطلوب:"
        send_section_with_image(chat_id, msg_id, 'vodafone', text_out, vodafone_markup())
        return

    if data == 'section_we':
        custom = get_setting('section_welcome_we', '')
        text_out = custom if custom else "🌐 قسم وي 🌐\n\n✨ اختر القسم المطلوب:"
        send_section_with_image(chat_id, msg_id, 'we', text_out, we_markup())
        return

    if data == 'section_natera':
        custom = get_setting('section_welcome_natera', '')
        text_out = custom if custom else "🧙 قسم النترا 🧙\n\n✨ اختر القسم المطلوب:"
        send_section_with_image(chat_id, msg_id, 'natera', text_out, natera_markup())
        return

    if data == 'section_orange':
        custom = get_setting('section_welcome_orange', '')
        text_out = custom if custom else "✨ قسم اورنج ✨\n\n✨ اختر القسم المطلوب:"
        send_section_with_image(chat_id, msg_id, 'orange', text_out, orange_markup())
        return

    if data == 'section_etisalat':
        custom = get_setting('section_welcome_etisalat', '')
        text_out = custom if custom else "📡 قسم اتصالات\n\n✨ اختر القسم المطلوب:"
        send_section_with_image(chat_id, msg_id, 'etisalat', text_out, etisalat_markup())
        return

    if data == 'section_tamween':
        try:
            bot.delete_message(chat_id, msg_id)
        except Exception:
            pass
        start_service_flow(chat_id, user_id, 'tamween')
        return

    if data == 'section_orders':
        try_edit_caption("📋 طلباتي\n\n✨ قائمة طلباتك:", orders_markup())
        return

    if data == 'section_referrals':
        ref_count = get_referral_count(user_id)
        last_ref = get_last_referral(user_id)
        try:
            me = bot.get_me()
            ref_link = f"https://t.me/{me.username}?start={user_id}"
        except Exception:
            ref_link = f"رابطك الخاص: /start {user_id}"
        ref_text = (
            f"👥 قسم الإحالات 👥\n\n"
            f"📊 عدد إحالاتك الحالية: {ref_count}\n"
            f"📈 إجمالي الإحالات: {ref_count}\n"
            f"📅 آخر إحالة: {last_ref}\n\n"
            f"🔗 رابط إحالتك الخاص:\n{ref_link}\n\n"
            f"💡 كيفية الاستخدام:\n"
            f"1. شارك الرابط مع أصدقائك\n"
            f"2. عندما يبدأ أحدهم البوت من رابطك تحصل على إحالة\n"
            f"3. اجمع الإحالات واستخدمها للدفع بالخدمات\n\n"
            f"🎁 الأقسام المتاحة للدفع بالإحالات:\n"
            f"• فودافون: 30 إحالة\n"
            f"• أورنج: 20 إحالة\n"
            f"• وي: 30 إحالة\n"
            f"• اتصالات: 60 إحالة\n"
            f"• تموين: 20 إحالة"
        )
        try_edit_caption(ref_text, referrals_markup())
        return

    if data == 'section_support':
        try_edit_caption("🛠 الدعم الفني\n\n✨ اختر نوع الاستفسار:", support_markup())
        return

    if data == 'section_admin':
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ ليس لديك صلاحية!", show_alert=True)
            return
        try_edit_caption("⚙️ لوحة التحكم\n\n✨ اختر الخيار المطلوب:", admin_markup())
        return

    # ==================== SERVICE START ====================
    if data.startswith('service_'):
        service_key = data[8:]
        if service_key in SERVICES:
            try:
                bot.delete_message(chat_id, msg_id)
            except Exception:
                pass
            start_service_flow(chat_id, user_id, service_key)
        return

    # ==================== CONFIRM / CANCEL ORDER ====================
    if data.startswith('confirm_order_'):
        service_key = data[14:]
        order_data = get_data(user_id, 'order_data')
        if not order_data:
            return
        cancel_countdown(user_id)

        service = order_data['service']
        order_id = order_data['order_id']
        section_id = order_data['section_id']
        wallet_num = order_data['wallet_num']
        wallet_name = order_data['wallet_name']
        target_num = order_data['target_num']
        price = order_data['price']

        success_text = (
            f"🆕 تم تأكيد الطلب بنجاح!\n\n"
            f"📋 رقم الطلب: #{order_id}\n"
            f"📋 رقم الطلب الخاص بالقسم: #{section_id}\n"
            f"📱 الخدمة: {service['service_code']}\n"
            f"📱 رقم المحفظة: {wallet_num}\n"
            f"🏦 اسم المحفظة: {wallet_name}\n"
            f"📞 الرقم: {target_num}\n"
            f"💰 المبلغ: {price} جنيه\n\n"
            f"✨ جاري مراجعة طلبك..."
        )
        try:
            bot.edit_message_caption(chat_id, msg_id, caption=success_text)
        except Exception:
            try:
                bot.edit_message_text(success_text, chat_id, msg_id)
            except Exception:
                bot.send_message(chat_id, success_text)

        notify_developer_order(chat_id, user_id, order_data)
        clear_state(user_id)
        return

    if data == 'cancel_order':
        cancel_countdown(user_id)
        clear_state(user_id)
        try:
            bot.edit_message_caption(chat_id, msg_id, caption="❌ تم إلغاء الطلب.")
        except Exception:
            try:
                bot.edit_message_text("❌ تم إلغاء الطلب.", chat_id, msg_id)
            except Exception:
                pass
        send_main_menu(chat_id, user_id)
        return

    # ==================== DEVELOPER ORDER ACTIONS ====================
    if data.startswith('dev_accept_') and not data.startswith('dev_accept_nopost_'):
        if not is_admin(user_id):
            return
        order_id = int(data[11:])
        # اسأل الأدمن عن التقييم قبل القبول
        RATING_OPTIONS = [
            ("⭐⭐⭐⭐⭐ ممتاز", "5"),
            ("⭐⭐⭐⭐ جيد جداً", "4"),
            ("⭐⭐⭐ جيد", "3"),
            ("⭐⭐ مقبول", "2"),
            ("⭐ ضعيف", "1"),
        ]
        markup = types.InlineKeyboardMarkup()
        for label, val in RATING_OPTIONS:
            markup.add(types.InlineKeyboardButton(label, callback_data=f"dev_rate_{order_id}_{val}"))
        markup.add(types.InlineKeyboardButton("⏭ قبول بدون نشر في قناة الثقة", callback_data=f"dev_accept_nopost_{order_id}"))
        bot.send_message(chat_id,
            f"⭐ اختر تقييم الخدمة للطلب #{order_id}\n"
            f"سيُنشر التقييم في قناة الثقة تلقائياً:",
            reply_markup=markup)
        return

    if data.startswith('dev_accept_nopost_'):
        if not is_admin(user_id):
            return
        order_id = int(data[18:])
        conn = get_db()
        conn.execute("UPDATE orders SET status='accepted' WHERE id=?", (order_id,))
        row = conn.execute('SELECT user_id FROM orders WHERE id=?', (order_id,)).fetchone()
        conn.commit()
        conn.close()
        if row:
            try:
                bot.send_message(row['user_id'], f"✅ تم قبول طلبك رقم #{order_id}! سيتم تنفيذ الخدمة قريباً.")
            except Exception:
                pass
        try:
            bot.edit_message_reply_markup(chat_id, msg_id, reply_markup=None)
        except Exception:
            pass
        bot.send_message(chat_id, f"✅ تم قبول الطلب #{order_id} بدون نشر في قناة الثقة.")
        return

    if data.startswith('dev_rate_'):
        if not is_admin(user_id):
            return
        parts = data.split('_')
        # dev_rate_{order_id}_{rating}
        order_id = int(parts[2])
        rating_val = parts[3]
        RATING_EMOJIS = {
            '5': '⭐⭐⭐⭐⭐',
            '4': '⭐⭐⭐⭐',
            '3': '⭐⭐⭐',
            '2': '⭐⭐',
            '1': '⭐',
        }
        rating_emoji = RATING_EMOJIS.get(rating_val, '⭐⭐⭐⭐⭐')
        conn = get_db()
        conn.execute("UPDATE orders SET status='accepted' WHERE id=?", (order_id,))
        order_row = conn.execute('SELECT * FROM orders WHERE id=?', (order_id,)).fetchone()
        conn.commit()
        conn.close()
        if order_row:
            target_uid = order_row['user_id']
            # احصل على اسم العميل
            client_conn = get_db()
            client_row = client_conn.execute('SELECT first_name, username FROM users WHERE user_id=?', (target_uid,)).fetchone()
            client_conn.close()
            if client_row:
                client_name = client_row['first_name'] or client_row['username'] or str(target_uid)
            else:
                client_name = str(target_uid)
            try:
                bot.send_message(target_uid, f"✅ تم قبول طلبك رقم #{order_id}! سيتم تنفيذ الخدمة قريباً.")
            except Exception:
                pass
            post_to_trust_channel(order_row, client_name, rating_emoji)
        try:
            bot.edit_message_reply_markup(chat_id, msg_id, reply_markup=None)
        except Exception:
            pass
        trust_set = get_setting('trust_channel_id', '')
        if trust_set:
            bot.send_message(chat_id, f"✅ تم قبول الطلب #{order_id} ونُشر في قناة الثقة بتقييم {rating_emoji}")
        else:
            bot.send_message(chat_id, f"✅ تم قبول الطلب #{order_id}\n⚠️ قناة الثقة غير مضبوطة بعد - اضبطها من لوحة الأدمن.")
        return

    if data.startswith('dev_reject_'):
        if not is_admin(user_id):
            return
        order_id = int(data[11:])
        conn = get_db()
        conn.execute("UPDATE orders SET status='rejected' WHERE id=?", (order_id,))
        row = conn.execute('SELECT user_id FROM orders WHERE id=?', (order_id,)).fetchone()
        conn.commit()
        conn.close()
        if row:
            try:
                bot.send_message(row['user_id'], f"❌ تم رفض طلبك رقم #{order_id}. للاستفسار راسل الدعم.")
            except Exception:
                pass
        try:
            bot.edit_message_reply_markup(chat_id, msg_id, reply_markup=None)
        except Exception:
            pass
        bot.send_message(chat_id, f"❌ تم رفض الطلب #{order_id}")
        return

    if data.startswith('dev_reply_'):
        if not is_admin(user_id):
            return
        order_id = int(data[10:])
        set_state(user_id, 'admin_reply_order', reply_order_id=order_id)
        bot.send_message(chat_id, "💬 أرسل رسالتك (نص أو صورة أو فيديو) للمستخدم:")
        return

    if data.startswith('dev_ticket_reply_'):
        if not is_admin(user_id):
            return
        ticket_id = int(data[17:])
        set_state(user_id, 'admin_reply_ticket', reply_ticket_id=ticket_id)
        bot.send_message(chat_id, "💬 أرسل ردك على التذكرة (نص أو صورة أو فيديو):")
        return

    # ==================== SUPPORT ====================
    if data in ['support_withdrawal', 'support_inquiry', 'support_suspicious']:
        type_map = {
            'support_withdrawal': 'وصف مشكلة في السحب',
            'support_inquiry': 'استفسار عن البوت',
            'support_suspicious': 'دعم البيانات المشكوك بها'
        }
        ticket_type = type_map[data]
        set_state(user_id, 'support_message', ticket_type=ticket_type, support_text='', support_photos=[])
        try:
            bot.delete_message(chat_id, msg_id)
        except Exception:
            pass
        bot.send_message(
            chat_id,
            f"📞 {ticket_type}\n\n"
            f"✨ اكتب وصف المشكلة أو الاستفسار الآن:\n\n"
            f"💎 يمكنك إرسال:\n"
            f"• رسالة نصية\n"
            f"• صور متعددة\n"
            f"• ثم اكتب \"تم\" عند الانتهاء"
        )
        return

    # ==================== ADMIN PANEL ====================
    if not is_admin(user_id):
        return

    if data == 'admin_users':
        bot.send_message(chat_id, f"👥 إجمالي المستخدمين: {get_user_count()}")
        return

    if data == 'admin_stats':
        pending_map = get_pending_orders_by_section()
        total_pending = sum(pending_map.values())
        bot.send_message(
            chat_id,
            f"📊 الاحصائيات\n\n"
            f"👥 المستخدمين: {get_user_count()}\n"
            f"📋 الطلبات الكلية: {get_all_orders_count()}\n"
            f"⏳ الطلبات المعلقة: {total_pending}\n"
            f"✅ الطلبات المقبوله: {get_accepted_orders_count()}\n"
            f"💳 رقم الكاش العام: {get_setting('global_transfer_num', '01214691014')}"
        )
        return

    if data == 'admin_broadcast':
        set_state(user_id, 'admin_broadcast')
        bot.send_message(chat_id, "📢 أرسل رسالة الإذاعة (نص أو صورة أو فيديو):")
        return

    if data == 'admin_edit_welcome':
        set_state(user_id, 'admin_edit_welcome')
        current = get_setting('welcome_text', '')
        bot.send_message(chat_id, f"✏️ أرسل نص رسالة الترحيب الجديدة:\n\nالحالية:\n{current[:200]}...")
        return

    if data == 'admin_edit_image':
        set_state(user_id, 'admin_edit_image')
        bot.send_message(chat_id, "🖼 أرسل رابط صورة الترحيب الجديدة:")
        return

    if data == 'admin_trust_channel':
        set_state(user_id, 'admin_trust_channel')
        current = get_setting('trust_channel_id', 'غير مضبوط')
        bot.send_message(
            chat_id,
            f"📡 <b>إعداد قناة الثقة</b>\n\n"
            f"الحالية: <code>{current}</code>\n\n"
            f"أرسل الـ ID الخاص بقناة الثقة\n"
            f"مثال: <code>-1001234567890</code>\n\n"
            f"⚠️ تأكد أن البوت مضاف كمشرف (أدمن) في القناة",
            parse_mode='HTML'
        )
        return

    if data == 'admin_setup_trust':
        set_state(user_id, 'admin_trust_channel')
        current = get_setting('trust_channel_id', 'غير مضبوط')
        bot.send_message(
            chat_id,
            f"📡 <b>إعداد قناة الثقة للتسليمات</b>\n\n"
            f"📌 القناة الحالية: <code>{current}</code>\n\n"
            f"📤 أرسل الـ ID الخاص بقناة الثقة:\n"
            f"مثال: <code>-1001234567890</code>\n\n"
            f"⚠️ البوت يجب أن يكون أدمناً في القناة\n"
            f"📌 عند قبول أي طلب سيُنشر تلقائياً في القناة مع:\n"
            f"  • اسم الخدمة\n"
            f"  • اسم العميل\n"
            f"  • التاريخ والوقت\n"
            f"  • تقييم الخدمة بالإيموجي",
            parse_mode='HTML'
        )
        return

    # ==================== إيقاف / تشغيل الأقسام ====================
    if data == 'admin_toggle_sections':
        _ALL_SECTIONS = ['vodafone', 'we', 'natera', 'orange', 'etisalat', 'tamween']
        m = types.InlineKeyboardMarkup()
        for sec in _ALL_SECTIONS:
            disabled = is_section_disabled(sec)
            status   = "⏸ موقوف" if disabled else "✅ شغّال"
            action   = "تشغيل" if disabled else "إيقاف"
            btn_style = 'success' if disabled else 'danger'
            btn_icon  = EMOJI[0]  if disabled else EMOJI[9]
            m.add(types.InlineKeyboardButton(
                f"{status}  ◀  {SECTION_NAMES_AR[sec]}  —  اضغط لـ{action}",
                callback_data=f"admin_toggle_sec_{sec}",
                style=btn_style, icon_custom_emoji_id=btn_icon
            ))
        m.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="section_admin",
            style='success', icon_custom_emoji_id=E_BACK))
        lines = []
        for sec in _ALL_SECTIONS:
            icon = "⏸" if is_section_disabled(sec) else "✅"
            lines.append(f"{icon} {SECTION_NAMES_AR[sec]}")
        txt = "⏸ <b>إيقاف / تشغيل الأقسام</b>\n\n" + "\n".join(lines) + "\n\nاضغط على القسم لتغيير حالته:"
        try:
            bot.edit_message_caption(chat_id, msg_id, caption=txt, reply_markup=m, parse_mode='HTML')
        except Exception:
            try:
                bot.edit_message_text(txt, chat_id, msg_id, reply_markup=m, parse_mode='HTML')
            except Exception:
                bot.send_message(chat_id, txt, reply_markup=m, parse_mode='HTML')
        return

    if data.startswith('admin_toggle_sec_'):
        sec_key  = data[len('admin_toggle_sec_'):]
        disabled = is_section_disabled(sec_key)
        new_val  = '0' if disabled else '1'
        set_setting(f'section_disabled_{sec_key}', new_val)
        sec_name = SECTION_NAMES_AR.get(sec_key, sec_key)
        state_ar = "✅ تم تشغيل" if new_val == '0' else "⏸ تم إيقاف"
        # تحديث القائمة
        _ALL_SECTIONS = ['vodafone', 'we', 'natera', 'orange', 'etisalat', 'tamween']
        m = types.InlineKeyboardMarkup()
        for sec in _ALL_SECTIONS:
            dis       = is_section_disabled(sec)
            stts      = "⏸ موقوف" if dis else "✅ شغّال"
            act       = "تشغيل"   if dis else "إيقاف"
            btn_style = 'success'  if dis else 'danger'
            btn_icon  = EMOJI[0]   if dis else EMOJI[9]
            m.add(types.InlineKeyboardButton(
                f"{stts}  ◀  {SECTION_NAMES_AR[sec]}  —  اضغط لـ{act}",
                callback_data=f"admin_toggle_sec_{sec}",
                style=btn_style, icon_custom_emoji_id=btn_icon
            ))
        m.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="section_admin",
            style='success', icon_custom_emoji_id=E_BACK))
        lines = []
        for sec in _ALL_SECTIONS:
            icon = "⏸" if is_section_disabled(sec) else "✅"
            lines.append(f"{icon} {SECTION_NAMES_AR[sec]}")
        txt = (
            f"{state_ar} قسم <b>{sec_name}</b> بنجاح!\n\n"
            "⏸ <b>إيقاف / تشغيل الأقسام</b>\n\n"
            + "\n".join(lines)
            + "\n\nاضغط على القسم لتغيير حالته:"
        )
        try:
            bot.edit_message_caption(chat_id, msg_id, caption=txt, reply_markup=m, parse_mode='HTML')
        except Exception:
            try:
                bot.edit_message_text(txt, chat_id, msg_id, reply_markup=m, parse_mode='HTML')
            except Exception:
                bot.send_message(chat_id, txt, reply_markup=m, parse_mode='HTML')
        return

    if data == 'admin_support_account':
        set_state(user_id, 'admin_support_account')
        bot.send_message(chat_id, "👤 أرسل يوزر حساب الدعم الفني:")
        return

    if data == 'admin_subscription':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 قناة تليجرام", callback_data="admin_sub_telegram"))
        markup.add(types.InlineKeyboardButton("🔗 لينك اخر", callback_data="admin_sub_link"))
        markup.add(types.InlineKeyboardButton("🗑 مسح قناة من الاشتراك الاجباري", callback_data="admin_sub_delete"))
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="section_admin"))
        bot.send_message(chat_id, "📌 إدارة الاشتراك الإجباري:", reply_markup=markup)
        return

    if data == 'admin_sub_telegram':
        set_state(user_id, 'admin_add_sub_telegram')
        bot.send_message(chat_id, "📢 أرسل يوزر القناة (مثال: @mychannel):")
        return

    if data == 'admin_sub_link':
        set_state(user_id, 'admin_add_sub_link')
        bot.send_message(chat_id, "🔗 أرسل رابط القناة أو الصفحة:")
        return

    if data == 'admin_sub_delete':
        subs = get_subscriptions()
        if not subs:
            bot.send_message(chat_id, "❌ لا توجد قنوات مضافة.")
            return
        markup = types.InlineKeyboardMarkup()
        for sub in subs:
            markup.add(types.InlineKeyboardButton(
                f"🗑 {sub['channel_name']}",
                callback_data=f"admin_del_sub_{sub['id']}"
            ))
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="admin_subscription"))
        bot.send_message(chat_id, "🗑 اختر القناة للحذف:", reply_markup=markup)
        return

    if data.startswith('admin_del_sub_'):
        sub_id = int(data[14:])
        conn = get_db()
        row = conn.execute('SELECT channel_name FROM subscriptions WHERE id=?', (sub_id,)).fetchone()
        conn.close()
        name = row['channel_name'] if row else str(sub_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ تأكيد الحذف", callback_data=f"admin_confirm_del_sub_{sub_id}"),
            types.InlineKeyboardButton("❌ إلغاء", callback_data="admin_subscription")
        )
        bot.send_message(chat_id, f"هل تريد حذف قناة '{name}'؟", reply_markup=markup)
        return

    if data.startswith('admin_confirm_del_sub_'):
        sub_id = int(data[22:])
        conn = get_db()
        conn.execute('DELETE FROM subscriptions WHERE id=?', (sub_id,))
        conn.commit()
        conn.close()
        bot.send_message(chat_id, "✅ تم حذف القناة من الاشتراك الإجباري.")
        return

    if data == 'admin_pending':
        pending = get_pending_orders_by_section()
        section_labels = {
            'orange': 'اورنج',
            'Etisalat_data': 'اتصالات',
            'we': 'وي',
            'we_data': 'وي بطايق',
            'vodafone_data': 'فودافون',
            'vodafone_vip': 'فودافون مميز',
            'vodafone_ownership': 'فودافون ملكية',
            'tamween': 'تموين',
            'natera': 'نترا',
        }
        text_out = "⏳ الطلبات المعلقه بالاقسام:\n\n"
        markup = types.InlineKeyboardMarkup()
        all_sections_pending = {
            'اورنج': 0, 'اتصالات': 0, 'وي': 0,
            'فودافون': 0, 'تموين': 0, 'نترا': 0
        }
        for code, cnt in pending.items():
            label = section_labels.get(code, code)
            for k in all_sections_pending:
                if label.startswith(k.split()[0]):
                    all_sections_pending[k] += cnt
                    break
            else:
                all_sections_pending[label] = all_sections_pending.get(label, 0) + cnt

        for label, cnt in all_sections_pending.items():
            text_out += f"{label}: {cnt} طلب معلق\n"
            markup.add(types.InlineKeyboardButton(
                f"{label} ({cnt} معلق)",
                callback_data=f"admin_view_pending_section_{label}"
            ))
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="section_admin"))
        bot.send_message(chat_id, text_out, reply_markup=markup)
        return

    if data.startswith('admin_view_pending_section_'):
        section_label = data[27:]
        code_map = {
            'اورنج': 'orange',
            'اتصالات': 'Etisalat_data',
            'وي': 'we',
            'فودافون': 'vodafone_data',
            'تموين': 'tamween',
            'نترا': 'natera',
        }
        code = code_map.get(section_label, section_label)
        conn = get_db()
        rows = conn.execute(
            "SELECT * FROM orders WHERE service_code=? AND status='pending' ORDER BY id DESC LIMIT 10",
            (code,)
        ).fetchall()
        conn.close()
        if not rows:
            bot.send_message(chat_id, "❌ لا توجد طلبات معلقة.")
            return
        for row in rows:
            row_text = (
                f"📋 طلب #{row['id']}\n"
                f"👤 المستخدم: {row['user_id']}\n"
                f"📱 الخدمة: {row['service_name']}\n"
                f"📱 رقم المحفظة: {row['wallet_num']}\n"
                f"🏦 اسم المحفظة: {row['wallet_name']}\n"
                f"📞 الرقم: {row['target_num']}\n"
                f"💰 المبلغ: {row['price']} جنيه\n"
                f"📅 التاريخ: {row['created_at']}"
            )
            m = developer_order_markup(row['id'])
            try:
                bot.send_photo(chat_id, row['receipt_file_id'], caption=row_text, reply_markup=m)
            except Exception:
                bot.send_message(chat_id, row_text, reply_markup=m)
        return

    if data == 'admin_admins':
        conn = get_db()
        admins = conn.execute('SELECT * FROM admins').fetchall()
        conn.close()
        markup = types.InlineKeyboardMarkup()
        for admin in admins:
            name = admin['username'] or str(admin['user_id'])
            row_btns = [types.InlineKeyboardButton(f"👤 {name}", callback_data="noop")]
            if admin['user_id'] != DEVELOPER_ID:
                row_btns.append(
                    types.InlineKeyboardButton("🗑 حذف", callback_data=f"admin_remove_admin_{admin['user_id']}")
                )
            markup.add(*row_btns)
        markup.add(types.InlineKeyboardButton("➕ إضافة مشرف", callback_data="admin_add_admin"))
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="section_admin"))
        bot.send_message(chat_id, "🛡 قسم إدارة المشرفين:", reply_markup=markup)
        return

    if data == 'admin_add_admin':
        set_state(user_id, 'admin_add_admin')
        bot.send_message(chat_id, "➕ أرسل يوزر أو ID المشرف الجديد:")
        return

    if data.startswith('admin_remove_admin_'):
        admin_uid = int(data[19:])
        if admin_uid == DEVELOPER_ID:
            bot.answer_callback_query(call.id, "❌ لا يمكن حذف المطور!", show_alert=True)
            return
        conn = get_db()
        conn.execute('DELETE FROM admins WHERE user_id=?', (admin_uid,))
        conn.commit()
        conn.close()
        bot.send_message(chat_id, f"✅ تم حذف المشرف {admin_uid}")
        return

    # ══════════════════════════════════════════════════
    # ── الميزات التسع الجديدة ── CALLBACKS ──
    # ══════════════════════════════════════════════════

    # 1. حظر مستخدم بالـ ID
    if data == 'admin_ban':
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ ليس لديك صلاحية!", show_alert=True)
            return
        set_state(user_id, 'admin_ban_id')
        bot.send_message(chat_id, "🚫 أرسل الـ ID الخاص بالمستخدم المراد حظره:")
        return

    # 2. فك حظر مستخدم
    if data == 'admin_unban':
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ ليس لديك صلاحية!", show_alert=True)
            return
        set_state(user_id, 'admin_unban_id')
        bot.send_message(chat_id, "✅ أرسل الـ ID الخاص بالمستخدم لفك حظره:")
        return

    # 3. قائمة المحظورين
    if data == 'admin_banned_list':
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ ليس لديك صلاحية!", show_alert=True)
            return
        banned = get_banned_users()
        if not banned:
            bot.send_message(chat_id, "✅ لا يوجد مستخدمون محظورون حالياً.")
            return
        lines = ["📋 <b>قائمة المحظورين:</b>\n"]
        for b in banned:
            name = b['first_name'] or 'بدون اسم'
            uname = f"@{b['username']}" if b['username'] else 'بدون يوزر'
            lines.append(f"• {name} | {uname} | <code>{b['user_id']}</code>")
        markup = types.InlineKeyboardMarkup()
        for b in banned:
            markup.add(types.InlineKeyboardButton(
                f"✅ فك حظر {b['user_id']}",
                callback_data=f"admin_quick_unban_{b['user_id']}", style='success'))
        bot.send_message(chat_id, '\n'.join(lines), reply_markup=markup, parse_mode='HTML')
        return

    # 4. إرسال رسالة لمستخدم معين
    if data == 'admin_msg_user':
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ ليس لديك صلاحية!", show_alert=True)
            return
        set_state(user_id, 'admin_msg_user_id')
        bot.send_message(chat_id, "📨 أرسل الـ ID الخاص بالمستخدم الذي تريد مراسلته:")
        return

    # 5. بحث عن مستخدم بالـ ID
    if data == 'admin_search_user':
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ ليس لديك صلاحية!", show_alert=True)
            return
        set_state(user_id, 'admin_search_user_id')
        bot.send_message(chat_id, "🔍 أرسل الـ ID الخاص بالمستخدم للبحث عنه:")
        return

    # 6. تغيير سعر خدمة
    if data == 'admin_change_price':
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ ليس لديك صلاحية!", show_alert=True)
            return
        markup = types.InlineKeyboardMarkup()
        for skey, svc in SERVICES.items():
            current_price = get_service_price(skey)
            markup.add(types.InlineKeyboardButton(
                f"{svc['emoji']} {svc['name']} | {current_price} جنيه",
                callback_data=f"admin_set_price_{skey}", style='primary'))
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="section_admin", style='danger'))
        bot.send_message(chat_id, "💲 اختر الخدمة لتغيير سعرها:", reply_markup=markup)
        return

    if data.startswith('admin_set_price_'):
        skey = data[16:]
        if skey in SERVICES:
            set_state(user_id, 'admin_change_price_val', price_service_key=skey)
            current = get_service_price(skey)
            bot.send_message(chat_id,
                f"💲 السعر الحالي لـ {SERVICES[skey]['name']}: {current} جنيه\n"
                f"✏️ أرسل السعر الجديد (بالأرقام فقط):")
        return

    # 7. ادمن قسم معين
    if data == 'admin_section_admin':
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ ليس لديك صلاحية!", show_alert=True)
            return
        sections = {
            'vodafone': 'فودافون', 'we': 'وي', 'natera': 'النترا',
            'orange': 'اورنج', 'etisalat': 'اتصالات', 'tamween': 'تموين'
        }
        markup = types.InlineKeyboardMarkup()
        for skey, sname in sections.items():
            conn = get_db()
            cnt = conn.execute('SELECT COUNT(*) as c FROM section_admins WHERE section=?', (skey,)).fetchone()['c']
            conn.close()
            markup.add(types.InlineKeyboardButton(
                f"🗂 {sname} ({cnt} ادمن)",
                callback_data=f"admin_sec_admin_manage_{skey}", style='primary'))
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="section_admin", style='danger'))
        bot.send_message(chat_id, "🗂 اختر القسم لإدارة مشرفيه:", reply_markup=markup)
        return

    if data.startswith('admin_sec_admin_manage_'):
        section = data[22:]
        sections = {
            'vodafone': 'فودافون', 'we': 'وي', 'natera': 'النترا',
            'orange': 'اورنج', 'etisalat': 'اتصالات', 'tamween': 'تموين'
        }
        sname = sections.get(section, section)
        conn = get_db()
        sec_admins = conn.execute('SELECT * FROM section_admins WHERE section=?', (section,)).fetchall()
        conn.close()
        markup = types.InlineKeyboardMarkup()
        for sa in sec_admins:
            markup.add(
                types.InlineKeyboardButton(f"👤 {sa['user_id']}", callback_data="noop"),
                types.InlineKeyboardButton("🗑 إزالة", callback_data=f"admin_rem_sec_admin_{sa['id']}",
                    style='danger')
            )
        markup.add(types.InlineKeyboardButton(
            "➕ إضافة ادمن لهذا القسم",
            callback_data=f"admin_add_sec_admin_{section}", style='success'))
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="admin_section_admin", style='danger'))
        text_out = f"🗂 مشرفو قسم {sname}:\n\nعدد المشرفين: {len(sec_admins)}"
        bot.send_message(chat_id, text_out, reply_markup=markup)
        return

    if data.startswith('admin_add_sec_admin_'):
        section = data[20:]
        set_state(user_id, 'admin_add_section_admin_id', sec_admin_section=section)
        sections = {
            'vodafone': 'فودافون', 'we': 'وي', 'natera': 'النترا',
            'orange': 'اورنج', 'etisalat': 'اتصالات', 'tamween': 'تموين'
        }
        bot.send_message(chat_id,
            f"➕ أرسل الـ ID الخاص بالشخص لتعيينه مشرفاً على قسم {sections.get(section, section)}:")
        return

    if data.startswith('admin_rem_sec_admin_'):
        sa_id = int(data[20:])
        conn = get_db()
        conn.execute('DELETE FROM section_admins WHERE id=?', (sa_id,))
        conn.commit()
        conn.close()
        bot.send_message(chat_id, "✅ تم إزالة ادمن القسم.")
        return

    # 8. الطلبات المقبولة
    if data == 'admin_accepted_orders':
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ ليس لديك صلاحية!", show_alert=True)
            return
        conn = get_db()
        accepted = conn.execute(
            "SELECT * FROM orders WHERE status='accepted' ORDER BY id DESC LIMIT 20"
        ).fetchall()
        conn.close()
        if not accepted:
            bot.send_message(chat_id, "📭 لا توجد طلبات مقبولة حتى الآن.")
            return
        lines = [f"✅ <b>آخر {len(accepted)} طلباً مقبولاً:</b>\n"]
        for o in accepted:
            lines.append(
                f"• #{o['id']} | {o['service_name']} | {o['target_num']} | {o['price']} جنيه | {o['created_at'][:10]}"
            )
        bot.send_message(chat_id, '\n'.join(lines), parse_mode='HTML')
        return

    # 9. عرض طلب بالرقم
    if data == 'admin_view_order':
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ ليس لديك صلاحية!", show_alert=True)
            return
        set_state(user_id, 'admin_view_order_id')
        bot.send_message(chat_id, "🔎 أرسل رقم الطلب الذي تريد عرضه:")
        return

    if data.startswith('admin_show_receipt_'):
        oid = int(data[19:])
        conn = get_db()
        row = conn.execute('SELECT receipt_file_id FROM orders WHERE id=?', (oid,)).fetchone()
        conn.close()
        if row and row['receipt_file_id']:
            try:
                bot.send_photo(chat_id, row['receipt_file_id'], caption=f"📤 إيصال الطلب #{oid}")
            except Exception:
                bot.send_message(chat_id, f"❌ تعذر إرسال الإيصال.")
        else:
            bot.send_message(chat_id, "❌ لا يوجد إيصال لهذا الطلب.")
        return

    # حظر/فك حظر سريع من نتيجة البحث
    if data.startswith('admin_quick_ban_'):
        target = int(data[16:])
        conn = get_db()
        conn.execute('UPDATE users SET is_banned = 1 WHERE user_id = ?', (target,))
        conn.commit()
        conn.close()
        bot.answer_callback_query(call.id, f"✅ تم حظر {target}", show_alert=True)
        try:
            bot.send_message(target, "🚫 تم حظرك من استخدام هذا البوت.")
        except Exception:
            pass
        return

    if data.startswith('admin_quick_unban_'):
        target = int(data[18:])
        conn = get_db()
        conn.execute('UPDATE users SET is_banned = 0 WHERE user_id = ?', (target,))
        conn.commit()
        conn.close()
        bot.answer_callback_query(call.id, f"✅ تم فك حظر {target}", show_alert=True)
        try:
            bot.send_message(target, "✅ تم رفع الحظر عنك، يمكنك استخدام البوت مجدداً.")
        except Exception:
            pass
        return

    if data.startswith('admin_quick_msg_'):
        target = int(data[16:])
        set_state(user_id, 'admin_msg_user_text', msg_target_id=target)
        bot.send_message(chat_id, f"✏️ أرسل الرسالة للمستخدم {target}:")
        return

    # ══════════════════════════════════════════════════

    if data == 'admin_add_section':
        set_state(user_id, 'admin_add_section_name')
        bot.send_message(chat_id, "➕ أرسل اسم القسم الجديد:")
        return

    if data == 'admin_sec_pos_above':
        set_state(user_id, 'admin_add_section_welcome', section_position='above')
        bot.send_message(chat_id, "✏️ أرسل رسالة الترحيب للقسم الجديد (أرسل '-' لتخطي):")
        return

    if data == 'admin_sec_pos_below':
        set_state(user_id, 'admin_add_section_welcome', section_position='below')
        bot.send_message(chat_id, "✏️ أرسل رسالة الترحيب للقسم الجديد (أرسل '-' لتخطي):")
        return

    if data == 'admin_manage_sections':
        conn = get_db()
        dyn_sections = conn.execute('SELECT * FROM dynamic_sections').fetchall()
        conn.close()
        markup = types.InlineKeyboardMarkup()
        static_secs = ['فودافون', 'وي', 'النترا', 'اورنج', 'اتصالات', 'تموين']
        for s in static_secs:
            markup.add(types.InlineKeyboardButton(f"📂 {s} (ثابت)", callback_data="noop"))
        for sec in dyn_sections:
            locked_icon = "🔒" if sec['is_locked'] else "🔓"
            markup.add(
                types.InlineKeyboardButton(f"📂 {sec['section_name']}", callback_data="noop"),
                types.InlineKeyboardButton(locked_icon, callback_data=f"admin_lock_section_{sec['id']}"),
                types.InlineKeyboardButton("🗑", callback_data=f"admin_delete_section_{sec['id']}")
            )
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="section_admin"))
        bot.send_message(chat_id, "📂 إدارة الأقسام:", reply_markup=markup)
        return

    if data.startswith('admin_lock_section_'):
        sec_id = int(data[19:])
        conn = get_db()
        row = conn.execute('SELECT is_locked FROM dynamic_sections WHERE id=?', (sec_id,)).fetchone()
        if row:
            new_lock = 0 if row['is_locked'] else 1
            conn.execute('UPDATE dynamic_sections SET is_locked=? WHERE id=?', (new_lock, sec_id))
            conn.commit()
            status = "مغلق 🔒" if new_lock else "مفتوح 🔓"
            bot.send_message(chat_id, f"✅ تم تغيير حالة القسم إلى: {status}")
        conn.close()
        return

    if data.startswith('admin_delete_section_'):
        sec_id = int(data[21:])
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ تأكيد", callback_data=f"admin_confirm_del_section_{sec_id}"),
            types.InlineKeyboardButton("❌ إلغاء", callback_data="admin_manage_sections")
        )
        bot.send_message(chat_id, "⚠️ هل تريد حذف هذا القسم؟", reply_markup=markup)
        return

    if data.startswith('admin_confirm_del_section_'):
        sec_id = int(data[26:])
        conn = get_db()
        conn.execute('DELETE FROM dynamic_sections WHERE id=?', (sec_id,))
        conn.execute('DELETE FROM dynamic_buttons WHERE section_id=?', (sec_id,))
        conn.commit()
        conn.close()
        bot.send_message(chat_id, "✅ تم حذف القسم.")
        return

    if data == 'admin_edit_section_welcome':
        sections = {
            'vodafone': 'فودافون', 'we': 'وي', 'natera': 'النترا',
            'orange': 'اورنج', 'etisalat': 'اتصالات', 'tamween': 'تموين'
        }
        markup = types.InlineKeyboardMarkup()
        for k, v in sections.items():
            markup.add(types.InlineKeyboardButton(v, callback_data=f"admin_edit_sec_welcome_{k}"))
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="section_admin"))
        bot.send_message(chat_id, "✏️ اختر القسم لتغيير رسالة الترحيب:", reply_markup=markup)
        return

    if data.startswith('admin_edit_sec_welcome_'):
        section_key = data[23:]
        set_state(user_id, 'admin_edit_sec_welcome', editing_section=section_key)
        bot.send_message(chat_id, f"✏️ أرسل رسالة الترحيب الجديدة لقسم {section_key}:")
        return

    if data == 'admin_edit_button_welcome':
        sections = {
            'vodafone': 'فودافون', 'we': 'وي', 'natera': 'النترا',
            'orange': 'اورنج', 'etisalat': 'اتصالات', 'tamween': 'تموين'
        }
        markup = types.InlineKeyboardMarkup()
        for k, v in sections.items():
            markup.add(types.InlineKeyboardButton(v, callback_data=f"admin_btn_sec_{k}"))
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="section_admin"))
        bot.send_message(chat_id, "✏️ اختر القسم:", reply_markup=markup)
        return

    if data.startswith('admin_btn_sec_'):
        section_key = data[14:]
        section_services = {k: v for k, v in SERVICES.items() if v['section'] == section_key}
        markup = types.InlineKeyboardMarkup()
        for k, svc in section_services.items():
            markup.add(types.InlineKeyboardButton(svc['name'], callback_data=f"admin_edit_btn_welcome_{k}"))
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="admin_edit_button_welcome"))
        bot.send_message(chat_id, "✏️ اختر الخدمة:", reply_markup=markup)
        return

    if data.startswith('admin_edit_btn_welcome_'):
        service_key = data[23:]
        set_state(user_id, 'admin_edit_btn_welcome', editing_service=service_key)
        bot.send_message(chat_id, f"✏️ أرسل رسالة الترحيب الجديدة للخدمة:")
        return

    if data == 'admin_change_cash':
        sections = {
            'vodafone': ('فودافون', '01214691014'),
            'we': ('وي', '01214691014'),
            'natera': ('النترا', '01559376830'),
            'orange': ('اورنج', '01559376830'),
            'etisalat': ('اتصالات', '01214691014'),
            'tamween': ('تموين', '01214691014'),
        }
        markup = types.InlineKeyboardMarkup()
        for k, (name, default) in sections.items():
            current = get_setting(f'cash_{k}', default)
            markup.add(types.InlineKeyboardButton(f"{name} | {current}", callback_data=f"admin_change_cash_sec_{k}"))
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="section_admin"))
        bot.send_message(chat_id, "💰 اختر القسم لتغيير رقم الكاش:", reply_markup=markup)
        return

    if data.startswith('admin_change_cash_sec_'):
        section = data[22:]
        set_state(user_id, 'admin_change_cash', cash_section=section)
        current = get_setting(f'cash_{section}', '')
        bot.send_message(chat_id, f"💰 رقم الكاش الحالي: {current}\nأرسل رقم الكاش الجديد:")
        return

    if data == 'admin_section_images':
        if not is_admin(user_id):
            return
        sections = {
            'main': 'الرئيسية / الترحيب',
            'vodafone': 'فودافون',
            'we': 'وي',
            'natera': 'النترا',
            'orange': 'اورنج',
            'etisalat': 'اتصالات',
            'tamween': 'تموين',
        }
        markup = types.InlineKeyboardMarkup()
        for k, v in sections.items():
            current_img = get_setting(f'image_{k}', '')
            has_icon = '🖼' if current_img else '⬜'
            markup.add(types.InlineKeyboardButton(
                f"{has_icon} {v}",
                callback_data=f"admin_set_img_{k}"
            ))
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="section_admin"))
        bot.send_message(
            chat_id,
            "🖼 <b>إدارة صور الأقسام</b>\n\n"
            "🖼 = لديه صورة مخصصة\n"
            "⬜ = يستخدم الصورة الافتراضية\n\n"
            "اختر القسم لتغيير صورته:",
            reply_markup=markup, parse_mode='HTML'
        )
        return

    if data.startswith('admin_set_img_'):
        if not is_admin(user_id):
            return
        section_key = data[14:]
        section_names = {
            'main': 'الرئيسية / الترحيب',
            'vodafone': 'فودافون', 'we': 'وي', 'natera': 'النترا',
            'orange': 'اورنج', 'etisalat': 'اتصالات', 'tamween': 'تموين',
        }
        sname = section_names.get(section_key, section_key)
        current = get_setting(f'image_{section_key}', 'غير محدد')
        set_state(user_id, 'admin_set_section_image', section_image_key=section_key)
        markup = types.InlineKeyboardMarkup()
        if current != 'غير محدد':
            markup.add(types.InlineKeyboardButton(
                "🗑 حذف الصورة المخصصة (استخدام الافتراضية)",
                callback_data=f"admin_del_img_{section_key}"
            ))
        bot.send_message(
            chat_id,
            f"🖼 تغيير صورة قسم <b>{sname}</b>\n\n"
            f"الحالية: {current}\n\n"
            f"أرسل رابط الصورة الجديدة:",
            reply_markup=markup, parse_mode='HTML'
        )
        return

    if data.startswith('admin_del_img_'):
        if not is_admin(user_id):
            return
        section_key = data[14:]
        set_setting(f'image_{section_key}', '')
        section_names = {
            'main': 'الرئيسية', 'vodafone': 'فودافون', 'we': 'وي', 'natera': 'النترا',
            'orange': 'اورنج', 'etisalat': 'اتصالات', 'tamween': 'تموين',
        }
        sname = section_names.get(section_key, section_key)
        bot.send_message(chat_id, f"✅ تم حذف الصورة المخصصة لقسم {sname}. سيستخدم الصورة الافتراضية.")
        clear_state(user_id)
        return

    if data == 'admin_colors':
        sections = ['فودافون', 'وي', 'النترا', 'اورنج', 'اتصالات', 'تموين']
        markup = types.InlineKeyboardMarkup()
        for section in sections:
            markup.add(
                types.InlineKeyboardButton(section, callback_data="noop"),
                types.InlineKeyboardButton("🔴", callback_data=f"admin_color_{section}_red"),
                types.InlineKeyboardButton("🟢", callback_data=f"admin_color_{section}_green"),
                types.InlineKeyboardButton("🔵", callback_data=f"admin_color_{section}_blue")
            )
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="section_admin"))
        bot.send_message(chat_id, "🎨 تغيير لون الأقسام والأزرار:", reply_markup=markup)
        return

    if data.startswith('admin_color_'):
        parts = data.split('_')
        color = parts[-1]
        section_name = '_'.join(parts[2:-1])
        color_emoji = {'red': '🔴', 'green': '🟢', 'blue': '🔵'}.get(color, '')
        set_setting(f'color_section_{section_name}', color)
        bot.send_message(chat_id, f"✅ تم تغيير لون {section_name} إلى {color_emoji}")
        return


# ==================== MAIN ====================
if __name__ == '__main__':
    print("🚀 جاري تشغيل البوت...")
    init_db()
    print("✅ قاعدة البيانات جاهزة")
    print(f"✅ البوت يعمل الآن!")
    bot.polling(none_stop=True, interval=0, timeout=20)
