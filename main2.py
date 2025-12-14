import os
from fastapi import FastAPI, Request
from telebot import types
from bot_instance import bot

PUBLIC_URL = os.getenv("PUBLIC_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "secret-path-123")

app = FastAPI()

@app.get("/")
async def root():
    return {"ok": True, "status": "running"}

@app.post(f"/webhook/{WEBHOOK_SECRET}")
async def telegram_webhook(request: Request):
    try:
        raw = await request.body()
        if not raw:
            return {"ok": False, "reason": "empty body"}
        update = types.Update.de_json(raw.decode("utf-8"))
        bot.process_new_updates([update])
        return {"ok": True}
    except Exception as e:
        print(f"[webhook] error: {e}")
        return {"ok": False, "error": str(e)}

@app.on_event("startup")
async def on_startup():
    try:
        bot.remove_webhook()
        if PUBLIC_URL:
            url = f"{PUBLIC_URL}/webhook/{WEBHOOK_SECRET}"
            bot.set_webhook(url=url)
            print(f"[startup] Webhook configurado en: {url}")
        else:
            print("[startup] PUBLIC_URL no definido; no se configuró webhook")
    except Exception as e:
        print(f"[startup] error set_webhook: {e}")

# Importa handlers AL FINAL para registrar los comandos
import handlers  # noqa
