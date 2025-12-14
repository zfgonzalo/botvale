from telebot import types
from bot_instance import bot

@bot.message_handler(commands=['eliminar'])
def eliminar_personaje(message: types.Message):
    bot.reply_to(message, "¡Personaje eliminado!")

@bot.message_handler(commands=['trade'])
def trade_personajes(message: types.Message):
    bot.reply_to(message, "¡Intercambio realizado!")

@bot.message_handler(commands=['regalar'])
def regalar_personaje(message: types.Message):
    bot.reply_to(message, "¡Personaje regalado!")
