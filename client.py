import asyncio
import websockets
import moonraker
import json
from flask import Flask, Request, render_template
import time

f = open("secrets.json")
data = json.load(f)
address = data['auth']['ip']
user = data['auth']['user']
passw = data['auth']['passw']
port = data['auth']['port']
ip = f'http://{address}'

app = Flask(__name__)

async def handler(websocket): #this function handles the notifications outputted by the webhook.
    while True: 
        message = await websocket.recv()
        message_json = json.loads(message)
        method = message_json['method']
        params = message_json['params']
        
        print(message_json)
        if method == 'notify_klippy_disconnected':
            print("Printer has been disconnected!")
        elif method == 'notify_gcode_response':
            print(params)

@app.route("/listener")          
async def webhooks():
    token = moonraker.authUser(ip, user, passw)
    url = f"ws://{address}:{port}/websocket?token={token[0]}"
    try:
        async with websockets.connect(url) as ws: # Connects to the Websocket, and starts the function that handles the websocket notifications.
            await handler(ws)
    except TimeoutError:
        print("Error,Timed out! Server might be down or server address is wrong.")

@app.route("/", methods = ['GET'])
def moonraker_start():
    all_services = moonraker.serverCheckServices(ip)[0]
    active_services = moonraker.serverCheckServices(ip)[1]
    unactive_services = moonraker.serverCheckServices(ip)[2]

    print(f"\n{len(all_services) - len(unactive_services)} / {len(all_services)} services are up.\n")
        
    while True:# this for loop checks if the getServerInfo function is able to get serverstats, if it can't then it wait 10 seconds.
        try:
            server_stats = moonraker.getServerInfo(ip)
            break
        except:
            print("Critical services might still be restarting, letting them restart.")
            time.sleep(10)


    printer_status = server_stats['printer_state']

    if printer_status != 'ready':
        print("Printer is ready")
    elif printer_status == 'ready':
        print("Printer is connected.")
        time.sleep(.5)
        

    return render_template('index.html', printer = printer_status )

