from os import path, getenv


class Config:
    API_ID = int(getenv('API_ID','28247126'))
    API_HASH = getenv('API_HASH','cd2e50ee0d30c1a69fcbc45588b9471b')
    BOT_TOKEN = getenv('BOT_TOKEN','7622447051:AAErToQUO6DsVLoJlbFkiGFQFiBHEeZqVNk')

config = Config()
