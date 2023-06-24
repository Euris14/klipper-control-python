import requests as rq
import json
import time
import threading
from flask import Flask, render_template
import os


def main():  # this is the main function were I call all functions.
    while True:  # this loop checks to see if the getServerInfo function works, if it throws an exception, than I can asume that the server is down, or the ip address is typed incorrectly.
        user_ip = input("Please input your servers ip address (10.7.1.1): ")
        ip = f'http://{user_ip}'
        try:
            rq.get(f'{ip}/')
            break
        except:
            print("Server is down.")
         
    serverCheckServices(ip)
    # this for loop checks if the getServerInfo function is able to get serverstats, if it can't then it wait 10 seconds.
    for i in range(2):
        try:
            server_stats = getServerInfo(ip)
            break
        except:
            print("Critical services might be down, letting them restart.")
        time.sleep(10)

    
    for c in server_stats:
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

    while server_stats['printer_state'] == 'startup':
        time.sleep(1)
        print("\nPrinter is starting up.")
        if server_stats['printer_state'] != 'ready':
            break

    print("\nPrinter has connected.")
    time.sleep(3)
    displayTools(ip)
    # checks getServerInfo function for klipper state, if its not ready, then restart firmware.
    
def displayTools(ip): # this function is meant to be initiated and shown across.
    tools = getTools(ip)
    os.system('cls')
    for tool in tools:
        tool_temp = toolTemperature(tool, ip)

        print(f"{tool} : {tool_temp}")
    time.sleep(.8)
        

def getTools(ip): #this function gets all available tools like in the temperature function.
    response = rq.get(f"{ip}/server/temperature_store")
    json_resp = response.json()
    tools = []
    for c in json_resp['result']:
        tools.append(c)
    return tools

def getServerInfo(ip):# this function gets server information, like cpu info and network info.
    get = ['/machine/system_info', '/printer/info']
    getResponse = rq.get(f'{ip}{get[0]}')
    json = getResponse.json()
    information = {}  # this dictionary holds all variables to be returned.
    # system_info directory holds all the information on the server host.
    system_info = json['result']['system_info']
    # CPU information
    cpu_info = system_info['cpu_info']
    processor = cpu_info['processor']
    device_name = cpu_info['model']
    # Network information
    network = system_info['network']
    host_ip = network['wlan0']['ip_addresses'][0]['address']
    # Distribution information
    distribution = system_info['distribution']
    distro_name = distribution['name']
    # SD information
    sd_info = system_info['sd_info']
    sd_size = sd_info['capacity']
    sd_name = sd_info['manufacturer']
    # Klipper state
    getResponse2 = rq.get(f"{ip}{get[1]}")  # gets reponse from /server/info
    json2 = getResponse2.json()
    # stores state of klipper, and checks if klippy is connected.
    if not json2['result']:
        printer_state = 'error'
        printer_message = json2['error']['message']
    else:
        printer_state = json2['result']['state']
        printer_message = json2['result']['state_message']

    # seperated and added at the bottom to be able to adjust array object positions.
    information.update({'host_ip': host_ip})
    information.update({'device_name': device_name})
    information.update({'distro_name': distro_name})
    information.update({'sd_size': sd_size})
    information.update({'sd_name': sd_name})
    information.update({'processor': processor})
    information.update({'printer_state': printer_state})
    information.update({'printer_message': printer_message})

    # returns the dictionary created by {"category":"data"}.
    return information


# sends post request to restart the printer's firmware.
def restartFirmware(ip):
    response = rq.post(f'{ip}/printer/firmware_restart')
    post_response_json = response.json()
    
    try:  # checks to see if there is a result. eventually want to check if it restarted correctly and is now connected.
        json['result']
    except:
        return 'ok'
    return 'failed'
    

# this function checks the ~current temperature out of all devices. (Want to implement this better, maybe multithreading?)
def toolTemperature(tool, ip):
    response = rq.get(f"{ip}/server/temperature_store")
    response_json = response.json()

    amountTemp = response_json['result'][tool]['temperatures']
    extruder_temp = response_json['result'][tool]['temperatures'][len(amountTemp) - 1]

    return extruder_temp
    time.sleep(1)


# this function checks all of the services up on moonraker, and tries to restart them
def serverCheckServices(ip):
    response = rq.get(f"{ip}/machine/system_info")
    response_json = response.json()
    # this dictionary holds all of the available services no matter if they are running or not.
    availableServices = response_json["result"]["system_info"]["available_services"]
    # this dictionary is a dict containing the services, and if they are running or not.
    service = response_json["result"]["system_info"]["service_state"]
    active = []
    not_active = []
    # for every service in all available services, check to see if they are running or not by check the services dict.
    for c in availableServices:
        serviceState = service[c]["active_state"]
        # checks serviceState bool, if true, than add to active dict to be returned, else, be sent to not active.
        if not serviceState == "active":
            not_active.append(c)
            print(f"{c} is down!")
            print(f'Restarting service now.10')

            rq.post(f"http://10.7.1.215/machine/services/restart?service={c}")
            
        elif serviceState:
            active.append(c)
            print(f"\r{c} is up and running!")
            time.sleep(.5)

    return availableServices, active, not_active


if __name__ == "__main__":
    main()


