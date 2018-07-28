# standard library imports

# third party imports
from channels.routing import route

# local imports
from events_feed.consumers import ws_message, ws_connect, ws_disconnect


channel_routing = [
    route("websocket.connect", ws_connect),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]
