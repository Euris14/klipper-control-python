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
            
@app.route("/")          
async def webhooks():
    token = moonraker.authUser(ip, user, passw)
    url = f"ws://{address}:{port}/websocket?token={token[0]}"
    try:
        async with websockets.connect(url) as ws: # Connects to the Websocket, and starts the function that handles the websocket notifications.
            await handler(ws)
    except TimeoutError:
        print("Timed out! Server might be down or server address is wrong.")

@app.route("/index", methods = ['GET'])
def moonraker_start():
    all_services = moonraker.serverCheckServices(ip)[0]
    active_services = moonraker.serverCheckServices(ip)[1]
    unactive_services = moonraker.serverCheckServices(ip)[2]
    print(f"\n{len(all_services) - len(unactive_services)} / {len(all_services)} services are up.\n")
    for service in active_services:
        print(f'{service} service is up and running!')
    for service in unactive_services:
        print(f'{service} service is down!')
        if moonraker.restartFirmware(ip):
            print(f'{service} service is being restarted. Might still not go up, if problem continues then check service in klipper.')
        
    while True:# this for loop checks if the getServerInfo function is able to get serverstats, if it can't then it wait 10 seconds.
        try:
            server_stats = moonraker.getServerInfo(ip)
            break
        except:
            print("Critical services might still be restarting, letting them restart.")
            time.sleep(10)

    for c in server_stats:# this for loop just prints the serverstats in succession.
        match c:
            case "host_ip":
                print(f'\nHost IP: {server_stats[c]}')
            case "processor":
                print(f'Processor Type: {server_stats[c]}')
            case "device_name":
                print(f'Device Model: {server_stats[c]}')
            case "distro_name":
                print(f'Distritbution: {server_stats[c]}')
            case "sd_name":
                print(f'SD Card Manufacturer: {server_stats[c]}')
            case "sd_size":
                print(f'SD Card Size: {server_stats[c]}')

    printer_status = server_stats['printer_state']

    while printer_status != 'ready':
        print("Printer is not ready!")
        time.sleep(0.2)
        if printer_status == 'shutdown':
            print(f"Printer status is currently: {printer_status}.")
        elif printer_status == 'startup':
            print(f"Printer status is currently: {printer_status}.")
            break
        elif printer_status == 'error':
            print(f"Printer status is currently: {printer_status}.")
        moonraker.restartFirmware(ip)
        time.sleep(8)
    if printer_status == 'ready':
        print("Printer is connected.")
        time.sleep(.5)
        print("Starting server.")

