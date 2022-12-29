from aiohttp import web
from views import index
import aiohttp_jinja2
import jinja2

app = web.Application()
app["websockets"] = {}
app.router.add_get("/", index)
web.run_app(app)