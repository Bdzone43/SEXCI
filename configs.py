from os import path, getenv


class Config:
    API_ID = int(getenv('API_ID','xxxx'))
    API_HASH = getenv('API_HASH','xxxx')
    BOT_TOKEN = getenv('BOT_TOKEN','xxxx')

config = Config()
