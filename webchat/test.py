# import redis

# r = redis.Redis(host="localhost", port=6379)


# r.set("France", "Paris")
# r.set("Germany", "Berlin")

# print(r.get("France"))
# print(r.get("Germany"))

class Foo():
    def __init__(self, fn, ln):
        self.fname = fn
        self.lname = ln

import redis
import json
import aiohttp
from aiohttp import web

websockets = {}
ws = web.WebSocketResponse()
websockets["user1"] = ws
pickled = json.dumps(websockets)