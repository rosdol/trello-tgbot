import telebot

from config import Config
from users import (
    create_user,
    show_users,
    load_users,
    get_all_users,
    get_user_by_telegram_id,
    save_users,
)
from trello_bot import (
    get_all_boards,
    get_board_by_name,
    get_boards_list,
    get_list_by_name,
    get_cards,
    get_list_by_id,
    get_board_by_id,
)

bot = telebot.TeleBot(Config.telegramApiKey)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, get_board())


@bot.message_handler(commands=['get_all_lists'])
def get_all_lists(message):
    bot.send_message(message.chat.id, get_all_boards())


@bot.message_handler(commands=['get_my_cards'])
def my_cards(message):
    answer = ''
    user = get_user_by_telegram_id(message.from_user.id)
    board = get_board_by_id(user.board_id)
    lst = get_list_by_id(board, user.list_id)
    for card in lst.list_cards():
        answer+=f'{card.name}\n\n'
    bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=['link_list_with_user'])
def link_list_with_user(message):
    reply_message = message.reply_to_message
    if reply_message is None:
        bot.reply_to(
            message,
            "Ответьте этой командой на сообщение пользователя"
        )
    else:
        global user
        global is_getcard
        create_user(reply_message.from_user.first_name, reply_message.from_user.id)
        user = get_user_by_telegram_id(reply_message.from_user.id)
        is_getcard = False
        select_board(message)
        

@bot.message_handler(commands=['newuser'])
def new_user(message):
    reply_message = message.reply_to_message
    if reply_message is None:
        bot.reply_to(
            message,
            "Ответьте этой командой на сообщение пользователя",
        )
    else:
        create_user(reply_message.from_user.first_name, reply_message.from_user.id)
        bot.reply_to(message, "Ок")


@bot.message_handler(commands=['allUsers'])
def all_users(message):
    bot.reply_to(message, str(get_all_users()))


@bot.message_handler(commands=['getcards'])
def all_boards(message):
    global is_getcard 
    is_getcard = True
    select_board(message)


def select_board(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    for board in get_all_boards():
        button = telebot.types.KeyboardButton(board.name)
        markup.add(button)
    bot.send_message(message.chat.id, "Выберите доску:", reply_markup=markup)
    bot.register_next_step_handler(message, select_list)


def select_list(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    global board
    global is_getcard
    global user
    if get_board_by_name(message.text) is False:
        bot.reply_to(message, "Нет такой доски")
        bot.register_next_step_handler(message, select_board)
        return
    board = get_board_by_name(message.text)
    if not is_getcard:
        user.board_id = board.id
    for list in get_boards_list(board):
        button = telebot.types.KeyboardButton(list.name)
        markup.add(button)
    bot.send_message(message.chat.id, "Выберите колонку:", reply_markup=markup)
    bot.register_next_step_handler(message, get_cards)


def get_cards(message):
    global board
    global is_getcard

    if get_list_by_name(board, message.text) is False:
            bot.reply_to(message, "Нет такой колонки")
            bot.register_next_step_handler(message, select_board)
            return
    lst = get_list_by_name(board, message.text)
    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    if is_getcard:
        answer = ''
        for card in lst.list_cards():
            answer+=f'{card.name}\n\n'
        if answer == '':
            answer = 'Тут пусто'
        bot.send_message(message.chat.id, answer, reply_markup=markup)
    else:
        global user
        user.list_id = lst.id
        save_users()
        bot.send_message(message.chat.id, '👍', reply_markup=markup)

bot.polling()
