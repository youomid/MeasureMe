# standard library imports

# third party imports
from channels import Group

# local imports


# Connected to websocket.connect
def ws_connect(message):
	# Accept the connection
	message.reply_channel.send({"accept": True})
	# Add to the chat group
	Group("events").add(message.reply_channel)

# Connected to websocket.receive
def ws_message(message):
	Group("events").send({
		"text": "[user] %s" % message.content['text'],
	})

# Connected to websocket.disconnect
def ws_disconnect(message):
	Group("events").discard(message.reply_channel)