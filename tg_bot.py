import telebot

import datetime

from trello import Card
import threading
from dateutil import parser as dateparser

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
    get_member_by_id,
)
import pytz
bot = telebot.TeleBot(Config.telegramApiKey)

timezone = pytz.timezone("Europe/Moscow")


@bot.message_handler(commands=['get_my_cards'])
def my_cards(message):
    user = get_user_by_telegram_id(message.from_user.id)
    if user is False:
        bot.reply_to(message, "У вас нет своего листа")
        return
    board = get_board_by_id(user.board_id)
    lst = get_list_by_id(board, user.list_id)
    member = get_member_by_id(user.board_id, user.trello_id)
    bot.send_message(message.chat.id, show_cards(lst, member.fetch_cards()))


@bot.message_handler(commands=['newuser'])
def link_list_with_user(message):
    print(message, '\n\n------------')
    reply_message = message.reply_to_message
    print(reply_message, '\n\n')
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


@bot.message_handler(commands=['get_all_cards'])
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
    bot.register_next_step_handler(message, get_card)


def get_card(message):
    global board
    global is_getcard

    if get_list_by_name(board, message.text) is False:
            bot.reply_to(message, "Нет такой колонки")
            bot.register_next_step_handler(message, select_board)
            return
    lst = get_list_by_name(board, message.text)
    if is_getcard:
        markup = telebot.types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, show_cards(lst), reply_markup=markup)
    else:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
        global members
        members = {}
        for member in board.all_members():
            members[member.full_name] = member.id
            button = telebot.types.KeyboardButton(member.full_name)
            markup.add(button)
        global user
        user.list_id = lst.id
        bot.send_message(message.chat.id, 'Выберите пользователя:', reply_markup=markup)
        bot.register_next_step_handler(message, get_trello_user)


def get_trello_user(message):
    global user
    global members
    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    user.trello_id = members[message.text]
    save_users()
    bot.send_message(message.chat.id, '👍', reply_markup=markup)

# member_id = 60d4ae0fb1fd0731df2ff8c4
def show_cards(lst, cards=[]):
    answer = f'{lst.name}\n------------------\n'
    for card in lst.list_cards():
        if card.due_date == '':
            answer+=f'{card.name}\n\n'
        else:
            date = card.due_date.astimezone(timezone)
            date_time = date.strftime('%H:%M %d.%m.%y')
            answer+=f'{card.name}\n ↳ до: {date_time}\n'
    if len(cards) > 0:
        answer += '------------------\nОбщие задания:\n------------------\n'
        for card in cards:
            if card['due'] is not None:
                date = dateparser.parse(card['due']).astimezone(timezone)
                date_time = date.strftime('%H:%M %d.%m.%y')
                answer+=f"{card['name']}\n ↳ до: {date_time}\n"
            else:
                answer+=f"{card['name']}\n\n"
    return answer

@bot.message_handler(commands=['getcards'])
def all_boards(message):
    global is_getcard
    is_getcard = True
    select_board(message)

try:
    bot.polling(none_stop=True)
except:
    pass