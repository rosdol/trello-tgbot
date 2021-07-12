from trello import TrelloClient
from config import Config

client = TrelloClient(
        api_key = Config.trelloApiKey,
        token = Config.trelloToken,
    )

def get_all_boards():
    return client.list_boards()


def get_board():
    all_boards = client.list_boards()
    last_board = all_boards[-1]
    return last_board.name

# if __name__ == "__main__":
#     print(type(get_board()))