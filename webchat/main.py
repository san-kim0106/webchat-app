from aiohttp import web
from views import index
import aiohttp_jinja2
import jinja2
import redis
import pickle

app = web.Application()
app["websockets"] = {}
app.router.add_get("/", index)
r = redis.Redis(host="localhost", port=6379)
r.set("websockets", pickle.dumps({}))
web.run_app(app)