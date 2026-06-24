import json
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    TypeHandler,
    filters,
    ContextTypes,
)
from telegram import Update as TelegramUpdate
from Information import BOT_TOKEN, DEVELOPER_ID, WEBHOOK_URL, PORT
from keep_alive import start_health_server, start_self_ping

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

DATA_FILE = "data.json"

WAITING_KEYWORD       = 0
WAITING_TEXT          = 1
WAITING_IMAGE_CHOICE  = 2
WAITING_IMAGE         = 3
WAITING_ADD_USER      = 4
WAITING_RESTORE_FILE  = 5
WAITING_BUTTON_CHOICE = 6
WAITING_BUTTON_COUNT  = 7
WAITING_BUTTON_TEXT   = 8
WAITING_BUTTON_URL    = 9
WAITING_EDIT_TEXT     = 10
WAITING_EDIT_IMAGE_NEW = 11

# ── Custom Emoji IDs ──────────────────────────────────────────────────────────
E_ADD       = "5877219383691972108"
E_LIST      = "5875462364110787088"
E_USERS     = "5771887475421090729"
E_STATS     = "5877485980901971030"
E_BACKUP    = "5884448719889240368"
E_RESTORE   = "5877410604225924969"
E_ADD_USER  = "5920090136627908485"
E_DEL_USER  = "5879896690210639947"
E_LIST_USR  = "5942877472163892475"
E_EDIT      = "5879841310902324730"
E_DELETE    = "5841541824803509441"
E_TEXT      = "5886330010054168711"
E_IMAGE     = "5888799736508454231"
E_BUTTONS   = "5875431869842985304"
E_YES       = "5776375003280838798"
E_NO        = "5778527486270770928"
E_CAMERA    = "5846024087033353251"
E_CLEAR     = "5879915802815107172"
E_KEYWORD   = "5839380464116175529"
E_BACK      = "5877341274863832725"
E_INFO      = "5879785854284599288"
E_WARN      = "5881702736843511327"
E_NUM_1     = "5900116262368841797"
E_NUM_2     = "5900006938271288826"
E_NUM_3     = "5798869482176779018"
E_NUM_4     = "5900108617327054997"
E_NUM_5     = "5960961389014028206"
E_NUM_6     = "5900120651825418289"
E_LINK      = "5877465816030515018"


# ── Data helpers ─────────────────────────────────────────────────────────────
def load_data() -> dict:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            data.setdefault("stats", {})
            return data
    return {"responses": {}, "authorized_users": [], "stats": {}}


def save_data(data: dict) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def is_authorized(user_id: int) -> bool:
    if user_id == DEVELOPER_ID:
        return True
    data = load_data()
    return user_id in data.get("authorized_users", [])


def set_state(context: ContextTypes.DEFAULT_TYPE, state) -> None:
    context.user_data["state"] = state


def clear_state(context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["state"] = None


def get_state(context: ContextTypes.DEFAULT_TYPE):
    return context.user_data.get("state")


def commit_response(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> str:
    keyword = context.user_data.get("keyword", "")
    text = context.user_data.get("response_text", "")
    image = context.user_data.get("response_image")
    buttons = context.user_data.get("buttons") or []
    data = load_data()
    data.setdefault("responses", {})[keyword.lower()] = {
        "text": text,
        "image": image,
        "buttons": buttons if buttons else None,
        "added_by": user_id,
    }
    save_data(data)
    context.user_data.clear()
    return keyword


def commit_edit(context: ContextTypes.DEFAULT_TYPE) -> str:
    keyword = context.user_data.get("editing_keyword", "")
    data = load_data()
    resp = data.get("responses", {}).get(keyword, {})

    edit_field = context.user_data.get("edit_field")
    if edit_field == "text":
        resp["text"] = context.user_data.get("response_text", resp.get("text", ""))
    elif edit_field == "image":
        resp["image"] = context.user_data.get("response_image")
    elif edit_field == "buttons":
        buttons = context.user_data.get("buttons") or []
        resp["buttons"] = buttons if buttons else None

    data["responses"][keyword] = resp
    save_data(data)
    context.user_data.clear()
    return keyword


def build_response_keyboard(buttons: list | None) -> InlineKeyboardMarkup | None:
    if not buttons:
        return None
    rows = []
    for b in buttons:
        emoji_id = b.get("icon_custom_emoji_id")
        btn = InlineKeyboardButton(
            text=b["text"],
            url=b["url"],
            icon_custom_emoji_id=emoji_id if emoji_id else None,
        )
        rows.append([btn])
    return InlineKeyboardMarkup(rows)


def extract_custom_emoji_id(message) -> str | None:
    if not message.entities:
        return None
    for entity in message.entities:
        if entity.type == "custom_emoji":
            return entity.custom_emoji_id
    return None


def strip_custom_emojis(message) -> str:
    text = message.text or ""
    if not message.entities:
        return text.strip()
    entities = sorted(
        [e for e in message.entities if e.type == "custom_emoji"],
        key=lambda e: e.offset,
        reverse=True,
    )
    for entity in entities:
        text = text[: entity.offset] + text[entity.offset + entity.length :]
    return text.strip()


# ── Main menu ─────────────────────────────────────────────────────────────────
def build_main_menu(user_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("اضافة رد", callback_data="add_response", icon_custom_emoji_id=E_ADD)],
        [InlineKeyboardButton("ردودي", callback_data="my_responses", icon_custom_emoji_id=E_LIST)],
    ]
    if user_id == DEVELOPER_ID:
        keyboard.append(
            [InlineKeyboardButton("ادارة المستخدمين", callback_data="manage_users", icon_custom_emoji_id=E_USERS)]
        )
        keyboard.append(
            [InlineKeyboardButton("إحصائيات", callback_data="stats", icon_custom_emoji_id=E_STATS)]
        )
        keyboard.append(
            [
                InlineKeyboardButton("نسخ احتياطي", callback_data="backup", icon_custom_emoji_id=E_BACKUP),
                InlineKeyboardButton("استعادة بيانات", callback_data="restore", icon_custom_emoji_id=E_RESTORE),
            ]
        )
    return InlineKeyboardMarkup(keyboard)


# ── Shared helpers ────────────────────────────────────────────────────────────
async def ask_button_choice(send_fn) -> None:
    keyboard = [
        [
            InlineKeyboardButton("نعم اضف ازرار", callback_data="btn_choice_yes", icon_custom_emoji_id=E_YES),
            InlineKeyboardButton("لا بدون ازرار", callback_data="btn_choice_no", icon_custom_emoji_id=E_NO),
        ]
    ]
    await send_fn(
        "تضيف ازرار مع الرد؟",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


def build_my_responses_view(user_resps: dict, context: ContextTypes.DEFAULT_TYPE) -> tuple[str, InlineKeyboardMarkup]:
    keys = list(user_resps.keys())
    context.user_data["my_resp_keys"] = keys

    text = "ردودك\n\n"
    keyboard = []
    for i, (kw, resp) in enumerate(user_resps.items()):
        text += f"الكلمة: {kw}\n"
        text += f"الرد: {resp['text']}\n"
        if resp.get("image"):
            text += "فيها صورة ✓\n"
        btns = resp.get("buttons") or []
        if btns:
            text += f"عدد الازرار: {len(btns)}\n"
        text += "─────────────────\n"
        keyboard.append([
            InlineKeyboardButton(f"تعديل ({kw})", callback_data=f"edit_resp_{i}", icon_custom_emoji_id=E_EDIT),
            InlineKeyboardButton(f"حذف ({kw})", callback_data=f"del_resp_{i}", icon_custom_emoji_id=E_DELETE),
        ])

    text += "\n/start للرجوع"
    return text, InlineKeyboardMarkup(keyboard)


# ── /start ────────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    context.user_data.clear()
    if not is_authorized(user_id):
        await update.message.reply_text(
            'اهلا بيك البوت تبع شاتات ببجي قـــنــصــل فقط لو لقيت البوت في اي شات تاني احنا غير مسئولين <tg-emoji emoji-id="5323738166711049440">🔍</tg-emoji>\n\n'
            'هتنزل يوزر الشخص و لو معانا هتلاقي البوت بيرد عليك ان الشخص معانا و يقولك رقم كاش الشخص <tg-emoji emoji-id="5274195706066781810">💯</tg-emoji>\n\n'
            'لو لقيت البوت رد عليك يبقا متتعاملش غير مع رقم الكاش اللي اترد عليك بيه و تضغط علي نفس اليوزر اللي انتا نزلته و البوت رد عليه\n'
            'لو نزلت يوزر و البوت مردش عليك يبقا الشخص دا مش معانا او منتحل خلي بالك كويس جدا من الناس دي <tg-emoji emoji-id="5938368005611195877">❤️</tg-emoji>',
            parse_mode="HTML",
        )
        return

    name = update.effective_user.first_name or ""
    await update.message.reply_text(
        f"اهلا {name} 👋",
        reply_markup=build_main_menu(user_id),
    )


# ── /cancel ───────────────────────────────────────────────────────────────────
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.clear()
    await update.message.reply_text("اتالغت العملية\n\n/start للرجوع")


# ── Callback query handler ────────────────────────────────────────────────────
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    logger.info(f"button_handler called | data={query.data if query else 'None'} | user={update.effective_user.id if update.effective_user else 'None'}")
    await query.answer()
    user_id = query.from_user.id

    if not is_authorized(user_id):
        await query.edit_message_text("مش مصرح ليك.")
        return

    data_key = query.data

    if data_key == "add_response":
        await query.edit_message_text(
            "ابعت الكلمة اللي لما حد يكتبها في الشات يطلع الرد\n\nمثال: احمد"
        )
        set_state(context, WAITING_KEYWORD)
        return

    elif data_key == "my_responses":
        data = load_data()
        user_resps = {
            k: v
            for k, v in data.get("responses", {}).items()
            if v.get("added_by") == user_id
        }
        if not user_resps:
            await query.edit_message_text(
                "مفيش ردود مضافة منك لحد دلوقتي\n\nاضغط /start للرجوع"
            )
        else:
            text, markup = build_my_responses_view(user_resps, context)
            await query.edit_message_text(text, reply_markup=markup)
        return

    elif data_key.startswith("del_resp_"):
        idx = int(data_key.split("_")[2])
        keys = context.user_data.get("my_resp_keys", [])
        if idx >= len(keys):
            await query.edit_message_text("حدث خطأ، جرب /start مرة تانية")
            return
        keyword = keys[idx]
        data = load_data()
        if keyword in data.get("responses", {}):
            resp = data["responses"][keyword]
            if resp.get("added_by") != user_id and user_id != DEVELOPER_ID:
                await query.edit_message_text("مش مصرح ليك تحذف الرد ده")
                return
            del data["responses"][keyword]
            data.get("stats", {}).pop(keyword, None)
            save_data(data)
            user_resps = {
                k: v
                for k, v in data.get("responses", {}).items()
                if v.get("added_by") == user_id
            }
            if not user_resps:
                await query.edit_message_text(
                    f"اتحذف الرد على كلمة ({keyword}) ✓\n\nمفيش ردود تانية\n\n/start للرجوع"
                )
            else:
                text, markup = build_my_responses_view(user_resps, context)
                await query.edit_message_text(
                    f"اتحذف الرد على كلمة ({keyword}) ✓\n\n" + text,
                    reply_markup=markup,
                )
        else:
            await query.edit_message_text("الرد ده مش موجود\n\n/start للرجوع")
        return

    elif data_key.startswith("edit_resp_"):
        idx = int(data_key.split("_")[2])
        keys = context.user_data.get("my_resp_keys", [])
        if idx >= len(keys):
            await query.edit_message_text("حدث خطأ، جرب /start مرة تانية")
            return
        keyword = keys[idx]
        data = load_data()
        resp = data.get("responses", {}).get(keyword)
        if not resp:
            await query.edit_message_text("الرد ده مش موجود\n\n/start للرجوع")
            return
        if resp.get("added_by") != user_id and user_id != DEVELOPER_ID:
            await query.edit_message_text("مش مصرح ليك تعدل الرد ده")
            return

        context.user_data["editing_keyword"] = keyword
        keyboard = [
            [InlineKeyboardButton("تعديل النص", callback_data="edit_what_text", icon_custom_emoji_id=E_TEXT)],
            [InlineKeyboardButton("تعديل الصورة", callback_data="edit_what_image", icon_custom_emoji_id=E_IMAGE)],
            [InlineKeyboardButton("تعديل الأزرار", callback_data="edit_what_buttons", icon_custom_emoji_id=E_BUTTONS)],
        ]
        await query.edit_message_text(
            f"تعديل الرد على كلمة ({keyword})\n\nاختار اللي عاوز تعدله",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    elif data_key == "edit_what_text":
        keyword = context.user_data.get("editing_keyword", "")
        context.user_data["edit_field"] = "text"
        await query.edit_message_text(
            f"ابعت النص الجديد للرد على كلمة ({keyword})\n\n/cancel للالغاء"
        )
        set_state(context, WAITING_EDIT_TEXT)
        return

    elif data_key == "edit_what_image":
        keyword = context.user_data.get("editing_keyword", "")
        context.user_data["edit_field"] = "image"
        keyboard = [
            [
                InlineKeyboardButton("ابعت صورة جديدة", callback_data="edit_img_new", icon_custom_emoji_id=E_CAMERA),
                InlineKeyboardButton("ازالة الصورة", callback_data="edit_img_remove", icon_custom_emoji_id=E_CLEAR),
            ]
        ]
        await query.edit_message_text(
            f"تعديل صورة الرد على كلمة ({keyword})",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    elif data_key == "edit_img_new":
        await query.edit_message_text("ابعت الصورة الجديدة\n\n/cancel للالغاء")
        set_state(context, WAITING_EDIT_IMAGE_NEW)
        return

    elif data_key == "edit_img_remove":
        keyword = context.user_data.get("editing_keyword", "")
        context.user_data["edit_field"] = "image"
        context.user_data["response_image"] = None
        commit_edit(context)
        await query.edit_message_text(
            f"اتشالت الصورة من الرد على كلمة ({keyword}) ✓\n\n/start للرجوع"
        )
        return

    elif data_key == "edit_what_buttons":
        keyword = context.user_data.get("editing_keyword", "")
        context.user_data["edit_field"] = "buttons"
        context.user_data["buttons"] = []
        keyboard = [
            [
                InlineKeyboardButton("نعم اضف ازرار", callback_data="btn_choice_yes", icon_custom_emoji_id=E_YES),
                InlineKeyboardButton("لا امسح الازرار", callback_data="edit_btn_clear", icon_custom_emoji_id=E_CLEAR),
            ]
        ]
        await query.edit_message_text(
            f"تعديل ازرار الرد على كلمة ({keyword})\n\nتضيف ازرار جديدة؟",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        set_state(context, WAITING_BUTTON_CHOICE)
        return

    elif data_key == "edit_btn_clear":
        keyword = context.user_data.get("editing_keyword", "")
        context.user_data["edit_field"] = "buttons"
        context.user_data["buttons"] = []
        commit_edit(context)
        await query.edit_message_text(
            f"اتشالت الازرار من الرد على كلمة ({keyword}) ✓\n\n/start للرجوع"
        )
        return

    elif data_key == "manage_users":
        if user_id != DEVELOPER_ID:
            await query.edit_message_text("المطور بس يقدر يدخل هنا")
            return
        keyboard = [
            [InlineKeyboardButton("اضافة مستخدم", callback_data="add_user", icon_custom_emoji_id=E_ADD_USER)],
            [InlineKeyboardButton("ازالة مستخدم", callback_data="remove_user", icon_custom_emoji_id=E_DEL_USER)],
            [InlineKeyboardButton("قائمة المستخدمين", callback_data="list_users", icon_custom_emoji_id=E_LIST_USR)],
            [InlineKeyboardButton("حذف ردود مستخدم", callback_data="del_resp_by_user", icon_custom_emoji_id=E_CLEAR)],
        ]
        await query.edit_message_text(
            "ادارة المستخدمين",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    elif data_key == "add_user":
        if user_id != DEVELOPER_ID:
            await query.edit_message_text("المطور بس يقدر يدخل هنا")
            return
        await query.edit_message_text(
            "ابعت ID المستخدم اللي عاوز تضيفه\n\nتقدر تعرفه من @userinfobot"
        )
        set_state(context, WAITING_ADD_USER)
        return

    elif data_key == "remove_user":
        if user_id != DEVELOPER_ID:
            await query.edit_message_text("المطور بس يقدر يدخل هنا")
            return
        data = load_data()
        authorized = data.get("authorized_users", [])
        if not authorized:
            await query.edit_message_text("مفيش مستخدمين مضافين\n\n/start للرجوع")
            return
        keyboard = [
            [InlineKeyboardButton(f"حذف {uid}", callback_data=f"del_user_{uid}", icon_custom_emoji_id=E_DEL_USER)]
            for uid in authorized
        ]
        await query.edit_message_text(
            "اختار المستخدم اللي عاوز تشيله",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    elif data_key.startswith("del_user_"):
        if user_id != DEVELOPER_ID:
            await query.edit_message_text("المطور بس يقدر يدخل هنا")
            return
        target_uid = int(data_key.split("_")[2])
        data = load_data()
        if target_uid in data.get("authorized_users", []):
            data["authorized_users"].remove(target_uid)
            before = len(data.get("responses", {}))
            data["responses"] = {
                k: v
                for k, v in data.get("responses", {}).items()
                if v.get("added_by") != target_uid
            }
            deleted = before - len(data["responses"])
            save_data(data)
            await query.edit_message_text(
                f"اتشال المستخدم {target_uid} ✓\n"
                f"اتحذف {deleted} رد مرتبط بيه\n\n/start للرجوع"
            )
        else:
            await query.edit_message_text("المستخدم ده مش موجود في القائمة")
        return

    elif data_key == "list_users":
        if user_id != DEVELOPER_ID:
            await query.edit_message_text("المطور بس يقدر يدخل هنا")
            return
        data = load_data()
        authorized = data.get("authorized_users", [])
        if not authorized:
            await query.edit_message_text("مفيش مستخدمين مضافين\n\n/start للرجوع")
        else:
            text = f"المستخدمين ({len(authorized)})\n\n"
            for uid in authorized:
                text += f"• {uid}\n"
            text += "\n/start للرجوع"
            await query.edit_message_text(text)
        return

    elif data_key == "del_resp_by_user":
        if user_id != DEVELOPER_ID:
            await query.edit_message_text("المطور بس يقدر يدخل هنا")
            return
        data = load_data()
        responses = data.get("responses", {})
        user_counts: dict[int, int] = {}
        for resp in responses.values():
            uid = resp.get("added_by")
            if uid is not None:
                user_counts[uid] = user_counts.get(uid, 0) + 1
        if not user_counts:
            await query.edit_message_text("مفيش ردود مضافة من أي حد\n\n/start للرجوع")
            return
        keyboard = [
            [InlineKeyboardButton(
                f"{uid}  ({count} رد)",
                callback_data=f"drbu_{uid}",
                icon_custom_emoji_id=E_USERS,
            )]
            for uid, count in user_counts.items()
        ]
        await query.edit_message_text(
            f"اختار المستخدم اللي عاوز تحذف ردوده ({len(user_counts)} مستخدم)",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    elif data_key.startswith("drbu_"):
        if user_id != DEVELOPER_ID:
            await query.edit_message_text("المطور بس يقدر يدخل هنا")
            return
        target_uid = int(data_key[5:])
        data = load_data()
        user_resps = {
            k: v
            for k, v in data.get("responses", {}).items()
            if v.get("added_by") == target_uid
        }
        if not user_resps:
            await query.edit_message_text(
                f"مفيش ردود للمستخدم {target_uid}\n\n/start للرجوع"
            )
            return
        keys = list(user_resps.keys())
        context.user_data["mgr_keys"] = keys
        context.user_data["mgr_uid"] = target_uid

        text = f"ردود المستخدم {target_uid} ({len(keys)} رد)\n\n"
        for kw, resp in user_resps.items():
            text += f"• الكلمة: {kw}\n  الرد: {resp['text'][:40]}\n"
        text += "\nاختار رد تحذفه أو احذف الكل"

        keyboard = [
            [InlineKeyboardButton(
                f"حذف ({kw})",
                callback_data=f"dro_{i}",
                icon_custom_emoji_id=E_DELETE,
            )]
            for i, kw in enumerate(keys)
        ]
        keyboard.append([
            InlineKeyboardButton(
                f"حذف الكل ({len(keys)} ردود)",
                callback_data=f"dra_{target_uid}",
                icon_custom_emoji_id=E_CLEAR,
            )
        ])
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return

    elif data_key.startswith("dro_"):
        if user_id != DEVELOPER_ID:
            await query.edit_message_text("المطور بس يقدر يدخل هنا")
            return
        idx = int(data_key[4:])
        keys = context.user_data.get("mgr_keys", [])
        target_uid = context.user_data.get("mgr_uid")
        if idx >= len(keys) or target_uid is None:
            await query.edit_message_text("حدث خطأ، جرب من أول\n\n/start للرجوع")
            return
        keyword = keys[idx]
        data = load_data()
        if keyword in data.get("responses", {}):
            del data["responses"][keyword]
            data.get("stats", {}).pop(keyword, None)
            save_data(data)
            keys.pop(idx)
            context.user_data["mgr_keys"] = keys
            if not keys:
                await query.edit_message_text(
                    f"اتحذف الرد ({keyword}) ✓\n\nمفيش ردود تانية للمستخدم {target_uid}\n\n/start للرجوع"
                )
                return
            user_resps = {
                k: v
                for k, v in data.get("responses", {}).items()
                if v.get("added_by") == target_uid
            }
            text = f"اتحذف الرد ({keyword}) ✓\n\nردود المستخدم {target_uid} ({len(keys)} رد)\n\n"
            for kw, resp in user_resps.items():
                text += f"• الكلمة: {kw}\n  الرد: {resp['text'][:40]}\n"
            text += "\nاختار رد تحذفه أو احذف الكل"
            keyboard = [
                [InlineKeyboardButton(
                    f"حذف ({kw})",
                    callback_data=f"dro_{i}",
                    icon_custom_emoji_id=E_DELETE,
                )]
                for i, kw in enumerate(keys)
            ]
            keyboard.append([
                InlineKeyboardButton(
                    f"حذف الكل ({len(keys)} ردود)",
                    callback_data=f"dra_{target_uid}",
                    icon_custom_emoji_id=E_CLEAR,
                )
            ])
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.edit_message_text("الرد ده مش موجود\n\n/start للرجوع")
        return

    elif data_key.startswith("dra_"):
        if user_id != DEVELOPER_ID:
            await query.edit_message_text("المطور بس يقدر يدخل هنا")
            return
        target_uid = int(data_key[4:])
        data = load_data()
        before = len(data.get("responses", {}))
        deleted_keys = [
            k for k, v in data.get("responses", {}).items()
            if v.get("added_by") == target_uid
        ]
        for k in deleted_keys:
            data.get("stats", {}).pop(k, None)
        data["responses"] = {
            k: v
            for k, v in data.get("responses", {}).items()
            if v.get("added_by") != target_uid
        }
        deleted = before - len(data["responses"])
        save_data(data)
        context.user_data.pop("mgr_keys", None)
        context.user_data.pop("mgr_uid", None)
        await query.edit_message_text(
            f"اتحذف كل ردود المستخدم {target_uid} ✓\n"
            f"عدد الردود المحذوفة: {deleted}\n\n/start للرجوع"
        )
        return

    elif data_key == "stats":
        if user_id != DEVELOPER_ID:
            await query.edit_message_text("المطور بس يقدر يدخل هنا")
            return
        data = load_data()
        stats = data.get("stats", {})
        responses = data.get("responses", {})
        if not stats:
            await query.edit_message_text(
                "مفيش إحصائيات لحد دلوقتي\nالبوت محتاج يرد على ناس الأول\n\n/start للرجوع"
            )
            return
        sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
        text = "📊 إحصائيات الكلمات\n\n"
        for kw, count in sorted_stats:
            bar = "█" * min(count, 10)
            text += f"• الكلمة: {kw}\n"
            text += f"  عدد المرات: {count} {bar}\n"
            if kw not in responses:
                text += "  ⚠️ الرد اتحذف\n"
            text += "\n"
        text += "/start للرجوع"
        await query.edit_message_text(text)
        return

    elif data_key == "backup":
        if user_id != DEVELOPER_ID:
            await query.edit_message_text("المطور بس يقدر يدخل هنا")
            return
        if not os.path.exists(DATA_FILE):
            await query.edit_message_text("مفيش بيانات محفوظة لحد دلوقتي\n\n/start للرجوع")
            return
        data = load_data()
        total_responses = len(data.get("responses", {}))
        total_users = len(data.get("authorized_users", []))
        await query.edit_message_text(
            f"بيتبعت النسخة الاحتياطية 💾\n\n"
            f"الردود: {total_responses}\n"
            f"المستخدمين: {total_users}"
        )
        with open(DATA_FILE, "rb") as f:
            await context.bot.send_document(
                chat_id=user_id,
                document=f,
                filename="bot_backup.json",
                caption="نسخة احتياطية من بيانات البوت\nاحتفظ بيها عشان تقدر تسترجع البيانات",
            )
        return

    elif data_key == "restore":
        if user_id != DEVELOPER_ID:
            await query.edit_message_text("المطور بس يقدر يدخل هنا")
            return
        await query.edit_message_text(
            "ابعت ملف النسخة الاحتياطية (bot_backup.json)\n\n"
            "⚠️ تنبيه: البيانات الحالية هتتبدل بالكامل\n\n"
            "/cancel للالغاء"
        )
        set_state(context, WAITING_RESTORE_FILE)
        return

    elif data_key == "image_yes":
        await query.edit_message_text("ابعت الصورة")
        set_state(context, WAITING_IMAGE)
        return

    elif data_key == "image_no":
        context.user_data["response_image"] = None
        await ask_button_choice(query.message.reply_text)
        set_state(context, WAITING_BUTTON_CHOICE)
        return

    elif data_key == "btn_choice_no":
        edit_field = context.user_data.get("edit_field")
        if edit_field == "buttons":
            keyword = commit_edit(context)
            await query.edit_message_text(
                f"اتحذفت الازرار من الرد على كلمة ({keyword}) ✓\n\n/start للرجوع"
            )
        else:
            keyword = commit_response(context, user_id)
            await query.edit_message_text(
                f"اتحفظ الرد على كلمة ({keyword}) ✓\n\n/start للرجوع"
            )
        return

    elif data_key == "btn_choice_yes":
        keyboard = [
            [
                InlineKeyboardButton("1", callback_data="btn_count_1", icon_custom_emoji_id=E_NUM_1),
                InlineKeyboardButton("2", callback_data="btn_count_2", icon_custom_emoji_id=E_NUM_2),
                InlineKeyboardButton("3", callback_data="btn_count_3", icon_custom_emoji_id=E_NUM_3),
            ],
            [
                InlineKeyboardButton("4", callback_data="btn_count_4", icon_custom_emoji_id=E_NUM_4),
                InlineKeyboardButton("5", callback_data="btn_count_5", icon_custom_emoji_id=E_NUM_5),
                InlineKeyboardButton("6", callback_data="btn_count_6", icon_custom_emoji_id=E_NUM_6),
            ],
        ]
        await query.edit_message_text(
            "كام زر عاوز تضيف؟",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        set_state(context, WAITING_BUTTON_COUNT)
        return

    elif data_key.startswith("btn_count_"):
        count = int(data_key.split("_")[2])
        context.user_data["button_count"] = count
        context.user_data["current_button_index"] = 0
        context.user_data.setdefault("buttons", [])
        await query.edit_message_text(
            "ابعت نص الزر الاول\n\n"
            "لو عندك ايموجي مميز من بريميوم ضيفه في الرسالة وهيتحط قبل نص الزر تلقائي"
        )
        set_state(context, WAITING_BUTTON_TEXT)
        return


# ── Conversation steps ────────────────────────────────────────────────────────
async def receive_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyword = update.message.text.strip()
    context.user_data["keyword"] = keyword
    await update.message.reply_text(
        f"الكلمة: {keyword}\n\nدلوقتي ابعت نص الرد اللي هيظهر في الشات"
    )
    set_state(context, WAITING_TEXT)


async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["response_text"] = update.message.text.strip()
    keyboard = [
        [
            InlineKeyboardButton("نعم اضف صورة", callback_data="image_yes", icon_custom_emoji_id=E_CAMERA),
            InlineKeyboardButton("لا بدون صورة", callback_data="image_no", icon_custom_emoji_id=E_NO),
        ]
    ]
    await update.message.reply_text(
        "تضيف صورة مع الرد؟",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    set_state(context, WAITING_IMAGE_CHOICE)


async def receive_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.photo:
        await update.message.reply_text("ابعت صورة فقط")
        return

    context.user_data["response_image"] = update.message.photo[-1].file_id
    await ask_button_choice(update.message.reply_text)
    set_state(context, WAITING_BUTTON_CHOICE)


async def receive_edit_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyword = context.user_data.get("editing_keyword", "")
    context.user_data["response_text"] = update.message.text.strip()
    commit_edit(context)
    await update.message.reply_text(
        f"اتعدل النص للرد على كلمة ({keyword}) ✓\n\n/start للرجوع"
    )


async def receive_edit_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.photo:
        await update.message.reply_text("ابعت صورة فقط\n\n/cancel للالغاء")
        return

    keyword = context.user_data.get("editing_keyword", "")
    context.user_data["response_image"] = update.message.photo[-1].file_id
    commit_edit(context)
    await update.message.reply_text(
        f"اتعدلت الصورة للرد على كلمة ({keyword}) ✓\n\n/start للرجوع"
    )


async def receive_button_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    idx = context.user_data.get("current_button_index", 0)

    emoji_id = extract_custom_emoji_id(update.message)
    clean_text = strip_custom_emojis(update.message) if emoji_id else update.message.text.strip()

    context.user_data[f"btn_text_{idx}"] = clean_text
    context.user_data[f"btn_emoji_{idx}"] = emoji_id

    if emoji_id:
        logger.info(f"Custom emoji detected for button {idx}: {emoji_id}, text: {clean_text}")
    else:
        logger.info(f"No custom emoji in button {idx}, text: {clean_text}")

    await update.message.reply_text(
        f"ابعت الرابط للزر {idx + 1}\n\nمثال: https://t.me/username"
    )
    set_state(context, WAITING_BUTTON_URL)


async def receive_button_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    idx = context.user_data.get("current_button_index", 0)
    total = context.user_data.get("button_count", 1)

    url = update.message.text.strip()
    if not (url.startswith("http://") or url.startswith("https://") or url.startswith("tg://")):
        await update.message.reply_text(
            "الرابط غير صح لازم يبدأ بـ https:// او http:// او tg://\n\nابعت الرابط تاني"
        )
        return

    btn_text = context.user_data.pop(f"btn_text_{idx}", "زر")
    btn_emoji = context.user_data.pop(f"btn_emoji_{idx}", None)
    btn_data = {"text": btn_text, "url": url}
    if btn_emoji:
        btn_data["icon_custom_emoji_id"] = btn_emoji
    context.user_data["buttons"].append(btn_data)
    context.user_data["current_button_index"] = idx + 1

    if idx + 1 < total:
        next_num = idx + 2
        await update.message.reply_text(
            f"اتحفظ الزر {idx + 1} ✓\n\nابعت نص الزر {next_num}"
        )
        set_state(context, WAITING_BUTTON_TEXT)
    else:
        edit_field = context.user_data.get("edit_field")
        if edit_field == "buttons":
            keyword = commit_edit(context)
            await update.message.reply_text(
                f"اتحدثت الازرار للرد على كلمة ({keyword}) مع {total} زر ✓\n\n/start للرجوع"
            )
        else:
            keyword = commit_response(context, user_id)
            await update.message.reply_text(
                f"اتحفظ الرد على كلمة ({keyword}) مع {total} زر ✓\n\n/start للرجوع"
            )


async def receive_add_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        new_uid = int(update.message.text.strip())
        if new_uid == DEVELOPER_ID:
            await update.message.reply_text("المطور عنده صلاحيات كاملة اصلا\n\n/start للرجوع")
            clear_state(context)
            return
        data = load_data()
        authorized = data.setdefault("authorized_users", [])
        if new_uid in authorized:
            await update.message.reply_text(f"المستخدم {new_uid} مضاف اصلا\n\n/start للرجوع")
        else:
            authorized.append(new_uid)
            save_data(data)
            await update.message.reply_text(
                f"اتضاف المستخدم {new_uid} ✓\n\n/start للرجوع"
            )
    except ValueError:
        await update.message.reply_text("ابعت رقم بس\n\nمثال: 123456789")
    clear_state(context)


async def receive_restore_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id != DEVELOPER_ID:
        clear_state(context)
        return

    if not update.message.document:
        await update.message.reply_text("ابعت ملف JSON بس\n\n/cancel للالغاء")
        return

    doc = update.message.document
    if not doc.file_name.endswith(".json"):
        await update.message.reply_text("الملف لازم يكون json.\n\n/cancel للالغاء")
        return

    try:
        file = await doc.get_file()
        file_bytes = await file.download_as_bytearray()
        restored_data = json.loads(file_bytes.decode("utf-8"))

        if "responses" not in restored_data or "authorized_users" not in restored_data:
            await update.message.reply_text(
                "الملف غلط او تالف تاكد انه نسخة احتياطية من البوت ده\n\n/cancel للالغاء"
            )
            return

        restored_data.setdefault("stats", {})
        save_data(restored_data)
        total_responses = len(restored_data.get("responses", {}))
        total_users = len(restored_data.get("authorized_users", []))
        await update.message.reply_text(
            f"اتعملت الاستعادة ✓\n\nالردود: {total_responses}\nالمستخدمين: {total_users}\n\n/start للرجوع"
        )
    except (json.JSONDecodeError, UnicodeDecodeError):
        await update.message.reply_text("الملف تالف\n\n/cancel للالغاء")
        return

    clear_state(context)


# ── Dispatchers ───────────────────────────────────────────────────────────────
async def text_dispatcher(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = get_state(context)
    if state == WAITING_KEYWORD:
        await receive_keyword(update, context)
    elif state == WAITING_TEXT:
        await receive_text(update, context)
    elif state == WAITING_ADD_USER:
        await receive_add_user(update, context)
    elif state == WAITING_BUTTON_TEXT:
        await receive_button_text(update, context)
    elif state == WAITING_BUTTON_URL:
        await receive_button_url(update, context)
    elif state == WAITING_EDIT_TEXT:
        await receive_edit_text(update, context)
    else:
        await keyword_handler(update, context)


async def photo_dispatcher(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = get_state(context)
    if state == WAITING_IMAGE:
        await receive_image(update, context)
    elif state == WAITING_EDIT_IMAGE_NEW:
        await receive_edit_image(update, context)


async def doc_dispatcher(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = get_state(context)
    if state == WAITING_RESTORE_FILE:
        await receive_restore_file(update, context)


# ── Group + Private message handler ───────────────────────────────────────────
async def keyword_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    chat_type = update.message.chat.type
    user_id = update.effective_user.id

    if chat_type == "private" and not is_authorized(user_id):
        return

    msg_text = update.message.text.strip().lower()
    data = load_data()
    responses = data.get("responses", {})

    if msg_text not in responses:
        return

    data.setdefault("stats", {})[msg_text] = data["stats"].get(msg_text, 0) + 1
    save_data(data)

    resp = responses[msg_text]
    text = resp["text"]
    reply_markup = build_response_keyboard(resp.get("buttons"))

    if resp.get("image"):
        await update.message.reply_photo(
            photo=resp["image"],
            caption=text,
            reply_markup=reply_markup,
        )
    else:
        await update.message.reply_text(text, reply_markup=reply_markup)


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.error("Exception while handling an update:", exc_info=context.error)

    async def log_all_updates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.info(
            f"UPDATE RECEIVED | id={update.update_id} | "
            f"message={update.message is not None} | "
            f"callback_query={update.callback_query is not None} | "
            f"data={update.callback_query.data if update.callback_query else '-'}"
        )

    application.add_error_handler(error_handler)
    application.add_handler(TypeHandler(Update, log_all_updates), group=-1)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.PHOTO, photo_dispatcher))
    application.add_handler(MessageHandler(filters.Document.ALL, doc_dispatcher))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_dispatcher))

    is_render = WEBHOOK_URL and "onrender.com" in WEBHOOK_URL

    if is_render:
        logger.info("Starting in WEBHOOK mode (Render)")
        start_self_ping(WEBHOOK_URL, interval_seconds=840)
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=BOT_TOKEN,
            webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}",
            drop_pending_updates=True,
        )
    else:
        logger.info("Starting in POLLING mode (Replit/local)")
        start_health_server(port=8080)
        application.run_polling(
            drop_pending_updates=False,
            allowed_updates=[
                "message",
                "callback_query",
                "my_chat_member",
                "chat_member",
            ],
        )


if __name__ == "__main__":
    main()
