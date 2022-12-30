import aiohttp
import pickle
import redis
from aiohttp import web
from datetime import date, datetime

async def index(request):
    r = redis.Redis(host="localhost", port=6379)
    ws = web.WebSocketResponse()
    ws_ready = ws.can_prepare(request)
    websockets = pickle.loads(r.get("websockets"))

    if not ws_ready.ok:
        s = open("templates/index.html", "r")
        return web.Response(text=s.read(), content_type="text/html")
    
    await ws.prepare(request)

    name = "user{}".format(len(websockets) + 1)

    await ws.send_json({"action": "date", "date": date.today().strftime("%B %d, %Y")})

    for other_ws in websockets.values():
        await other_ws.send_json({'action': 'join', 'name': name})

    websockets[name] = ws # Save the current WS in the dict
    print(websockets)
    r.set("websockets", pickle.dumps(websockets))

    # Receive the message and propagate to all other users
    while True:
        msg = await ws.receive()

        if msg.type == aiohttp.WSMsgType.text:
            for other_ws in websockets.values():
                if other_ws == ws: continue
                await other_ws.send_json({"action": "sent_to_me", "name": name, "text": msg.data, "time": datetime.now().strftime("%H:%M")})
        else:
            break
    
    del websockets[name]
    for ws in request.app['websockets'].values():
        await ws.send_json({'action': 'disconnect', 'name': name})
    
    return ws