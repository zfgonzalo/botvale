import random
import os
import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from characters import characters

current_character = None
last_rc_time = {}

def get_tier_name(rarity):
    if rarity == 1:
        return "🌟 LEGENDARIO"
    elif rarity == 5:
        return "💜 ÉPICO"
    elif rarity == 15:
        return "💙 RARO"
    elif rarity == 30:
        return "💚 POCO COMÚN"
    else:
        return "⚪ COMÚN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎴 ¡Bienvenido al Gacha de Anime!\n\n"
        "Comandos disponibles:\n"
        "• #rc o #randomcharacter - Obtener un personaje aleatorio\n"
        "• #claim o #c - Reclamar el personaje mostrado\n"
        "• #mc o #mycharacters - Ver tus personajes\n"
        "• #cinfo <nombre> - Info de un personaje\n\n"
        f"📊 Personajes disponibles: {len(characters)}"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_character
    
    text = update.message.text.lower().strip()
    
    if not text.startswith("#"):
        return
    
    comando = text[1:]
    
    if comando in ["rc", "randomcharacter"]:
        user_id = update.message.from_user.id
        now = datetime.datetime.now()

        # COOLDOWN DESACTIVADO PARA PRUEBAS
        # if user_id in last_rc_time:
        #     diff = now - last_rc_time[user_id]
        #     if diff.total_seconds() < 15 * 60:
        #         tiempo_restante = int((15*60 - diff.total_seconds()) / 60) + 1
        #         await update.message.reply_text(f"⏳ Espera {tiempo_restante} minutos antes de usar #rc de nuevo.")
        #         return

        # last_rc_time[user_id] = now
        
        pesos = [char.rarity for char in characters]
        personaje = random.choices(characters, weights=pesos, k=1)[0]
        current_character = personaje

        tier = get_tier_name(personaje.rarity)

        reply = (
            f"🎴 PERSONAJE ENCONTRADO\n\n"
            f"👤 Nombre: {personaje.name}\n"
            f"📺 Anime: {personaje.anime}\n"
            f"⚧ Género: {personaje.gender}\n"
            f"🎯 Rareza: {tier} ({personaje.rarity}%)\n"
            f"📌 Estado: {personaje.status}\n\n"
            f"✍️ Usa #claim o #c para reclamarlo"
        )
        try:
            with open(personaje.image_path, 'rb') as photo_file:
                await update.message.reply_photo(photo=photo_file, caption=reply)
        except Exception:
            await update.message.reply_text(reply)

    elif comando in ["claim", "c"]:
        if current_character is None:
            await update.message.reply_text("❌ Primero usa #rc para obtener un personaje")
            return
            
        personaje = current_character
        
        if personaje.owner is None:
            personaje.owner = update.message.from_user.username
            personaje.status = "Reclamado"
            await update.message.reply_text(f"🎉 @{personaje.owner} reclamó a {personaje.name}!")
        else:
            await update.message.reply_text(f"❌ Este personaje ya fue reclamado por @{personaje.owner}")

    elif comando in ["mc", "mycharacters"]:
        username = update.message.from_user.username
        mis_personajes = [c for c in characters if c.owner == username]
        
        if not mis_personajes:
            await update.message.reply_text("📭 No tienes personajes reclamados todavía.\nUsa #rc para obtener uno!")
            return
        
        lista = "📜 **Tus personajes reclamados:**\n\n"
        for i, p in enumerate(mis_personajes, 1):
            tier = get_tier_name(p.rarity)
            lista += f"{i}. {p.name} - {tier}\n"
        
        lista += f"\n📊 Total: {len(mis_personajes)} personajes"
        await update.message.reply_text(lista)

    elif comando.startswith("cinfo ") or comando.startswith("characterinfo "):
        nombre_buscar = comando.split(" ", 1)[1].strip().lower()
        
        personaje_encontrado = None
        for c in characters:
            if nombre_buscar in c.name.lower():
                personaje_encontrado = c
                break
        
        if not personaje_encontrado:
            await update.message.reply_text(f"❌ No encontré ningún personaje con el nombre '{nombre_buscar}'")
            return
        
        tier = get_tier_name(personaje_encontrado.rarity)
        estado = f"Reclamado por @{personaje_encontrado.owner}" if personaje_encontrado.owner else "Disponible"
        
        reply = (
            f"📋 **INFORMACIÓN DEL PERSONAJE**\n\n"
            f"👤 Nombre: {personaje_encontrado.name}\n"
            f"📺 Anime: {personaje_encontrado.anime}\n"
            f"⚧ Género: {personaje_encontrado.gender}\n"
            f"🎯 Rareza: {tier} ({personaje_encontrado.rarity}%)\n"
            f"📌 Estado: {estado}"
        )
        
        try:
            with open(personaje_encontrado.image_path, 'rb') as photo_file:
                await update.message.reply_photo(photo=photo_file, caption=reply)
        except Exception:
            await update.message.reply_text(reply)

def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    
    if not token:
        print("ERROR: Necesitas configurar TELEGRAM_BOT_TOKEN")
        return
    
    print("Iniciando bot de Telegram...")
    print(f"Personajes cargados: {len(characters)}")
    
    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot corriendo!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
