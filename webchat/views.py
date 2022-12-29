import aiohttp
from aiohttp import web
from datetime import date, datetime

async def index(request):
    ws = web.WebSocketResponse()
    ws_ready = ws.can_prepare(request)

    if not ws_ready.ok:
        s = open("templates/index.html", "r")
        return web.Response(text=s.read(), content_type="text/html")
    
    await ws.prepare(request)

    name = "user{}".format(len(request.app["websockets"]) + 1)

    await ws.send_json({"action": "date", "date": date.today().strftime("%B %d, %Y")})

    for other_ws in request.app["websockets"].values():
        await other_ws.send_json({'action': 'join', 'name': name})

    request.app['websockets'][name] = ws # Save the current WS in the dict

    # Receive the message and propagate to all other users
    while True:
        msg = await ws.receive()

        if msg.type == aiohttp.WSMsgType.text:
            for other_ws in request.app["websockets"].values():
                if other_ws == ws: continue
                await other_ws.send_json({"action": "sent_to_me", "name": name, "text": msg.data, "time": datetime.now().strftime("%H:%M")})
        else:
            break
    
    del request.app["websockets"][name]
    for ws in request.app['websockets'].values():
        await ws.send_json({'action': 'disconnect', 'name': name})
    
    return ws