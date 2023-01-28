from walrus import *
from walrus import Cache as WalrusCache
from poliwag.settings import REDIS_HOST, REDIS_PORT

Cache = Walrus(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

walrus = WalrusCache(Cache)
