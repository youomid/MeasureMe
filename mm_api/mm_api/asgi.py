# standard library imports
import os

# third party imports
import channels.asgi

# local imports


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mm_api.settings")
channel_layer = channels.asgi.get_channel_layer()