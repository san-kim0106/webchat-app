from aiohttp import web
from views import index

app = web.Application()
app["websockets"] = {}
app.router.add_get("/", index)
web.run_app(app)