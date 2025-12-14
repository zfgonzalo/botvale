from telebot import types
from bot_instance import bot
from characters import characters

def find_character_by_name(name: str):
    name = name.strip().lower()
    for c in characters:
        if c.name.lower() == name:
            return c
    return None

@bot.message_handler(commands=['eliminar'])
def eliminar_personaje(message: types.Message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Uso: /eliminar <nombre del personaje>")
        return
    pj = find_character_by_name(parts[1])
    if not pj:
        bot.reply_to(message, "Personaje no encontrado 😕")
        return
    pj.status = "Disponible"
    pj.owner = None
    bot.reply_to(message, f"{pj.name} fue eliminado ✅")

@bot.message_handler(commands=['trade'])
def trade_personajes(message: types.Message):
    parts = message.text.split(' ', 2)
    if len(parts) < 3 or not parts[2].startswith('@'):
        bot.reply_to(message, "Uso: /trade <nombre> @usuario")
        return
    pj = find_character_by_name(parts[1])
    if not pj:
        bot.reply_to(message, "Personaje no encontrado 😕")
        return
    pj.owner = parts[2]
    pj.status = "Asignado"
    bot.reply_to(message, f"{pj.name} ahora pertenece a {parts[2]} 🔁")

@bot.message_handler(commands=['regalar'])
def regalar_personaje(message: types.Message):
    parts = message.text.split(' ', 2)
    if len(parts) < 3 or not parts[2].startswith('@'):
        bot.reply_to(message, "Uso: /regalar <nombre> @usuario")
        return
    pj = find_character_by_name(parts[1])
    if not pj:
        bot.reply_to(message, "Personaje no encontrado 😕")
        return
    pj.owner = parts[2]
    pj.status = "Asignado"
    bot.reply_to(message, f"¡{pj.name} fue regalado a {parts[2]}! 🎁")

