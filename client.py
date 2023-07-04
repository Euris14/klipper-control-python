import asyncio
import websockets
from moonraker import authUser
import json
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

token = authUser(server_address, user, passw) 

async def handler(websocket):
    while True: # Checks
        message = await websocket.recv()
        message_json = json.loads(message)
        print(message_json['method'])
        if message_json['method'] == 'notify_klippy_disconnected':
            print("Printer has been disconnected!")
        if message_json['method'] == 'notify_gcode_response':
            if '!! Must home axis first' in message_json['params']:
                print("Print was canceled, must home axis!")
            else:
                print(message_json['params'])


async def main():
    url = f"ws://10.7.1.215:7125/websocket?token={token[0]}"
    try:
        async with websockets.connect(url) as ws: # Connects to the Websocket, and starts the function that handles the websocket notifications.
            await handler(ws)
    except TimeoutError:
        print("Timed out! Server might be down or server address is wrong.")



if __name__ == "__main__":
    asyncio.run(main())