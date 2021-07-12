import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    trelloToken = os.environ.get('trelloToken')
    trelloApiKey = os.environ.get('trelloApiKey')
    telegramApiKey = os.environ.get('telegramApiKey')
