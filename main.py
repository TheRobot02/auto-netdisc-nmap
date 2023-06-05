#python 3.11.3

# Bronnen:
# Openai 
# w3schools
# https://pypi.org/project/mac-vendor-lookup/
# https://pypi.org/project/netifaces/
# https://pypi.org/project/python-nmap/
# https://www.programiz.com/python-programming/datetime/current-datetime

#------------[Imports]------------#
try:
    from configparser import ConfigParser 
    from components import Startup_check, NetDiscovery, filter_list, filter_ip_addresses, nmap_custom_scan
    from os import path
    from sys import version_info
except ModuleNotFoundError as e:
    print(f"missing modual {e}.\nExiting!")
    exit()
    

#-----[pyhton version check]-----#
if version_info <= (3, 11):
    print("Python 3.11 or later is required to run this code.")
    exit()
    
#-----[local variables]-----#
startup = Startup_check()
netdiscovery = NetDiscovery() 
config = ConfigParser()




#------------[main]------------#
if __name__ == "__main__":
    startup.startup_list()
    devices = netdiscovery.discover_devices()
    for device in devices:
        print(f"IP: {device['ip']}\t MAC: {device['mac']}\t VENDOR: {device['vendor']}")
    filterd_devices_ip = filter_list(devices)
    nmap_custom_scan(filterd_devices_ip)