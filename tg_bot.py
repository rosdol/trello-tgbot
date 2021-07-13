import telebot

from config import Config
from users import create_user, show_users, load_users, get_all_users
from trello_bot import get_board, get_all_boards

bot = telebot.TeleBot(Config.telegramApiKey)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, get_board())


@bot.message_handler(commands=['get_all_lists'])
def get_all_lists(message):
    bot.send_message(message.chat.id, get_all_boards())


@bot.message_handler(commands=['new_user'])
def new_user(message):
    reply_message = message.reply_to_message
    if reply_message is None:
        bot.reply_to(message, "Ответьте этой командой на сообщение пользователя")
    else:
        create_user(reply_message.from_user.first_name, reply_message.from_user.id)
        bot.reply_to(message, "Ок")


@bot.message_handler(commands=['load_users'])
def loadusers(message):
    load_users()


@bot.message_handler(commands=['allUsers'])
def all_users(message):
    bot.reply_to(message, str(get_all_users()))


@bot.message_handler(commands=['allBoards'])
def all_boards(message):
    bot.reply_to(message, str(get_all_boards()))

bot.polling()
