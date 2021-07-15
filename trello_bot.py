from trello import TrelloClient
from config import Config

client = TrelloClient(
        api_key = Config.trelloApiKey,
        token = Config.trelloToken,
    )

def get_all_boards():
    return client.list_boards()


def get_board_by_name(name):
    boards = get_all_boards()
    for board in boards:
        if board.name.lower() == name.lower():
            return board
    return False


def get_board_by_id(id):
    boards = get_all_boards()
    for board in boards:
        if board.id == id:
            return board
    return False


def get_boards_list(board):
    return board.list_lists()


def get_list_by_name(board, name):
    lists = get_boards_list(board)
    for lst in lists:
        if lst.name.lower() == name.lower():
            return lst
    return False


def get_list_by_id(board, id):
    lists = get_boards_list(board)
    for lst in lists:
        if lst.id == id:
            return lst
    return False


def get_cards(lst):
    return lst.list_cards()


def get_card_by_name(lst, name):
    cards = get_cards(lst)
    for card in cards:
        if card.name.lower() == name.lower():
            return card
    return False
