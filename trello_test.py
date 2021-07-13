from trello_bot import (
    get_all_boards,
    get_board,
    get_board_by_name,
    get_boards_list,
    get_list_by_name,
    get_card_by_name,
)

if __name__ == "__main__":
    board = get_board_by_name('Test ApI')
    lst = get_list_by_name(board, 'testo')
    card = get_card_by_name(lst, 'Mhm')
    print(card.set_reminder(120))