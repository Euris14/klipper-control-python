import requests as rq
import time
import os
def authUser(ip, user, passw): # this function gets the user and pass, and returns the user token.
    pack = {
    "username": f'{user}',
    "password": f'{passw}',
    "source": "moonraker"
    }
    login = rq.post(f"{ip}/access/login", params= pack, headers= {"Content-Type": "application/json"} )

    json = login.json()['result']
    token = json['token']
    refresh_token = json['refresh_token']

    return token, refresh_token
    
def displayTools(ip):
    tools = getTools(ip)
    for tool in tools:
        tool_temp = toolTemperature(tool, ip)
        print(f"{tool} : {tool_temp}")
    time.sleep(.8)
    os.system('cls')

def getTools(ip):# this function gets all available tools like in the temperature function.
    response = rq.get(f"{ip}/server/temperature_store")
    json_resp = response.json()
    tools = []
    for c in json_resp['result']:
        tools.append(c)
    return tools

def getServerInfo(ip):# this function gets server information, like cpu info, network info.
    get = ['/machine/system_info', '/server/info']
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
    response = rq.get(f"{ip}{get[1]}")  # gets reponse from /server/info
    response_json = response.json()
    # stores printer state, and checks if klipper is connected.
    klippy_state = response_json['result']['klippy_state']
    is_klippy_connected = response_json['result']['klippy_connected']
    components = response_json['result']['components']


    # seperated and added at the bottom to be able to adjust array object positions.
    information.update({'host_ip': host_ip})
    information.update({'device_name': device_name})
    information.update({'distro_name': distro_name})
    information.update({'sd_size': sd_size})
    information.update({'sd_name': sd_name})
    information.update({'processor': processor})
    information.update({'klippy_state': klippy_state})
    information.update({'printer_connection': is_klippy_connected})
    information.update({'components' : components})

    
    return information # returns the dictionary created by {"category":"data"}.
def restartService(ip,service):
    rq.post(f'{ip}/machine/services/restart?service={service}')

def restartFirmware(ip):# sends post request to restart the printer's firmware.
    response = rq.post(f'{ip}/printer/firmware_restart')
    response_json = response.json()
    try:# checks to see if there is a result. eventually want to check if it restarted correctly and is now connected.
        response_json['result']
    except:
        return False
    return True

def toolTemperature(tool, ip):# this function checks the ~current temperature out of all devices. 
    response = rq.get(f"{ip}/server/temperature_store")
    response_json = response.json()

    temperatures = response_json['result'][tool]['temperatures']
    tool_temperature = response_json['result'][tool]['temperatures'][len(temperatures) - 1]

    return tool_temperature

def serverCheckServices(ip):# this function checks all of the services up on moonraker, and tries to restart them
    response = rq.get(f"{ip}/machine/system_info")
    response_json = response.json()
    # this dictionary holds all of the available services no matter if they are running or not.
    available_services = response_json["result"]["system_info"]["available_services"]
    # this dictionary is a dict containing the services, and if they are running or not.
    service_state = response_json["result"]["system_info"]["service_state"]

    active = []
    not_active = []
    
    for c in available_services:# for every service in all available services, check to see if they are running or not by check the services dict.
        service = service_state[c]["active_state"]
        if not service == "active":# checks serviceState bool, if true, than add to active dict to be returned, else, be sent to not active.
            not_active.append(c)
        elif service:
            active.append(c)

    
    return available_services, active, not_active

def serverState(ip): # this function returns the full server ip, and checks if the ip passed will throw an exception (Most likely wrong ip or server not up.)
    server_ip = f'http://{ip}'
    try:
        rq.get(f'{server_ip}/')
        return server_ip
    except:
        return False
    
def rootDirectory(ip): # this function returns all of the root directories on the server.
    response = rq.get(f'{ip}/server/files/roots')
    response_json = response.json()

    file_amount = len(response_json['result'])
    root_directories = (response_json['result'])

    return root_directories, file_amount

def directoryContents(ip, dir):
    response = rq.get(f'{ip}/server/files/list?root={dir}')
    response_json = response.json()
    file_index = response_json['result']

    return file_index 

def gcodeMetadata(ip, file):
    response = rq.get(f'{ip}/server/files/metadata?filename={file}')
    response_json = response.json()

    metadata = response_json['result']
    return metadata


