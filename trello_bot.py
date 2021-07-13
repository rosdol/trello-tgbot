from trello import TrelloClient
from config import Config

client = TrelloClient(
        api_key = Config.trelloApiKey,
        token = Config.trelloToken,
    )

def get_all_boards():
    answer = ''
    for board in client.list_boards():
        answer+=f'{board.name}\n'
    return answer


def get_board():
    all_boards = client.list_boards()
    last_board = all_boards[-1]
    return last_board.name


def get_board_by_name(name):
    boards = get_all_boards()
    for board in boards:
        if board.name.lower() == name.lower():
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
# if __name__ == "__main__":
#     print(type(get_board()))

def get_cards(lst):
    return lst.list_cards()


def get_card_by_name(lst, name):
    cards = get_cards(lst)
    for card in cards:
        if card.name.lower() == name.lower():
            return card
    return False
