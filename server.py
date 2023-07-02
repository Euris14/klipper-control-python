import moonraker
import sys
import time
"""
This is the main module for this app. In this module you will find the functions that
connect you to the moonraker server, starts a django or flask server with the custom
made moonraker api.
"""

def moonraker_start(server_ip): #this function connects to the printer and checks if it's up!

    if not moonraker.serverState(server_ip):
        return f'Printer could not connect to {server_ip}. \nCheck if server is down, or ip is correct and re-run.'
    else:
        print("Server was found!")
        ip = moonraker.serverState(server_ip)

    all_services = moonraker.serverCheckServices(ip)[0]
    active_services = moonraker.serverCheckServices(ip)[1]
    unactive_services = moonraker.serverCheckServices(ip)[2]
    print(f"\n{len(all_services) - len(unactive_services)} / {len(all_services)} services are up.\n")
    for service in active_services:
        print(f'{service} service is up and running!.')
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
        return ip

if __name__ == "__main__":
    try:
        ip = sys.argv[1]
        full_ip = moonraker_start(ip)
    except:
        print("Proper usage: python server.py {server}.")
    
    

