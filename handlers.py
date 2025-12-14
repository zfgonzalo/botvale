from telebot import types
from bot_instance import bot
from characters import characters

# Buscar personaje por nombre
def find_character_by_name(name: str):
    name = name.strip().lower()
    for c in characters:
        if c.name.lower() == name:
            return c
    return None

# ---------- COMANDOS ----------

@bot.message_handler(commands=['eliminar'])
def eliminar_personaje(message: types.Message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Uso: /eliminar <nombre del personaje>")
        return

    personaje = find_character_by_name(parts[1])
    if not personaje:
        bot.reply_to(message, "Personaje no encontrado 😕")
        return

    personaje.status = "Disponible"
    personaje.owner = None
    bot.reply_to(message, f"{personaje.name} fue eliminado ✅")


@bot.message_handler(commands=['trade'])
def trade_personajes(message: types.Message):
    parts = message.text.split(' ', 2)
    if len(parts) < 3:
        bot.reply_to(message, "Uso: /trade <nombre> @usuario")
        return

    personaje = find_character_by_name(parts[1])
    if not personaje:
        bot.reply_to(message, "Personaje no encontrado 😕")
        return

    personaje.owner = parts[2]
    personaje.status = "Asignado"
    bot.reply_to(message, f"{personaje.name} ahora pertenece a {parts[2]} 🔁")


@bot.message_handler(commands=['regalar'])
def regalar_personaje(message: types.Message):
    parts = message.text.split(' ', 2)
    if len(parts) < 3:
        bot.reply_to(message, "Uso: /regalar <nombre> @usuario")
        return

    personaje = find_character_by_name(parts[1])
    if not personaje:
        bot.reply_to(message, "Personaje no encontrado 😕")
        return

    personaje.owner = parts[2]
    personaje.status = "Asignado"
    bot.reply_to(message, f"{personaje.name} fue regalado a {parts[2]} 🎁")
