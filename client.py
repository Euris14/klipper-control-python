import asyncio
import websockets
import moonraker
import json
from flask import Flask, request, render_template, redirect
import time

f = open("secrets.json")
data = json.load(f)
address = data['auth']['ip']
ip = f'http://{address}'

app = Flask(__name__)

@app.route("/button", methods=["GET", "POST"])
def restartFirmware():
    if request.method == 'POST':
        if request.form.get('submit_button') == 'Firmware Restart':
            moonraker.restartFirmware(ip)
        if request.form.get('submit_button') == 'Restart Klipper':
            moonraker.restartService(ip, service= 'klipper')
    time.sleep(9)
    return redirect("/")

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
            
          
async def webhooks():
    user = data['auth']['user']
    passw = data['auth']['passw']
    port = data['auth']['port']

    token = moonraker.authUser(ip, user, passw)
    url = f"ws://{address}:{port}/websocket?token={token[0]}"
    try:
        async with websockets.connect(url) as ws: # Connects to the Websocket, and starts the function that handles the websocket notifications.
            await handler(ws)
    except TimeoutError:
        print("Error, timed out! Server might be down or server address is wrong.")

@app.route("/", methods = ['GET'])
def moonraker_start():    
    while True:
        try:
            server_info = moonraker.getServerInfo(ip)
            break
        except:
            print("Critical services might still be restarting, letting them restart.")
            time.sleep(10)


    printer_status = server_info['printer_connection']
    klippy_status = server_info['klippy_state']

    nonactive_services = moonraker.serverCheckServices(ip)[2]
    total_services = moonraker.serverCheckServices(ip)[0]
    if printer_status:
        if klippy_status == 'ready':
            return render_template("index.html")
        elif klippy_status != 'ready':
            return render_template("klippy.html", klippy_state = klippy_status, connection = printer_status )
    if not printer_status:
        print(klippy_status)
        
    

if __name__ == "__main__":
    app.run("0.0.0.0", "5000")
    
    

    