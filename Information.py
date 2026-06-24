import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8902866238:AAF_Yv3iyXtXguRZUozVWBVpzVcMlXb4aoU")
DEVELOPER_ID = int(os.environ.get("DEVELOPER_ID", "7654693261"))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")
PORT = int(os.environ.get("PORT", "8080"))

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN غير موجود! ضيفه في Secrets.")
