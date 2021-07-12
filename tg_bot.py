import telebot

from config import Config
from users import create_user, show_users
from trello_bot import get_board, get_all_boards

bot = telebot.TeleBot(Config.telegramApiKey)

tg_id_dict = {}

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, get_board())


@bot.message_handler(commands=['get_all_lists'])
def get_all_lists(message):
    bot.send_message(message.chat.id, get_all_boards())


@bot.message_handler(commands=['new_user'])
def new_user(message):
    bot.reply_to(message, "Перешли сообщение этого пользователя чтобы я его запомнил")
    bot.register_next_step_handler(message, new_user_step2)
    # create_user('Susan')
    # bot.send_message(message.chat.id, show_users())


def new_user_step2(message):
    chat_id = message.chat.id
    tg_id_dict[chat_id] = message.forward_from.id
    bot.reply_to(
        message,
        "Как назовем пользователя?",
    )
    bot.register_next_step_handler(
        message, 
        new_user_step3,
    )


def new_user_step3(message):
    chat_id = message.chat.id
    create_user(message.text, tg_id_dict[chat_id])
    show_users()



bot.polling()
