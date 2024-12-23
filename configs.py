from os import path, getenv


class Config:
    API_ID = int(getenv('API_ID','23104928'))
    API_HASH = getenv('API_HASH','af6425de587ed34c1b9071e26ccbf7e5')
    BOT_TOKEN = getenv('BOT_TOKEN','7679006349:AAFM1bMmafYTQHXL-8SicF0gsxHUqdL1h_E')

config = Config()
