#!/usr/bin/python
# made with python 3.11

# sources:
# Openai 
# w3schools
# https://pypi.org/project/mac-vendor-lookup/
# https://pypi.org/project/netifaces/
# https://pypi.org/project/python-nmap/
# https://www.programiz.com/python-programming/datetime/current-datetime

#------------[Imports]------------#
try:
    from configparser import ConfigParser 
    from components import StartupCheck, NetDiscovery, filter_list, nmap_custom_scan
    from sys import version_info
except ModuleNotFoundError as e:
    print(f"missing modual {e}.\nExiting!")
    exit()
    

#-----[pyhton version check]-----#
if version_info <= (3, 11):
    print("Python 3.11 or later is required to run this code.")
    exit()
    
#-----[global variables]-----#
startup = StartupCheck()
netdiscovery = NetDiscovery() 
config = ConfigParser()




#------------[main]------------#
if __name__ == "__main__":
    try:
        startup.startup_list()
        devices = netdiscovery.discover_devices()
        filterd_devices_ip = filter_list(devices)
        nmap_custom_scan(filterd_devices_ip)
    except KeyboardInterrupt:
        print("\nProgram interrupted by the user.\nExiting")
        exit()