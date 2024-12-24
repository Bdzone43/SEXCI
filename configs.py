from os import path, getenv


class Config:
    API_ID = int(getenv('API_ID','21603683'))
    API_HASH = getenv('API_HASH','c531b0ec35017b19e043cf9f106ed95b')
    BOT_TOKEN = getenv('BOT_TOKEN','7622447051:AAErToQUO6DsVLoJlbFkiGFQFiBHEeZqVNk')

config = Config()
