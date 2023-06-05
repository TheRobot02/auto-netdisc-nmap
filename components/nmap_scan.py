try:
    from configparser import ConfigParser 
    from datetime import datetime
    import nmap
except ModuleNotFoundError as e:
    print(f"nmap_scan. {e}.\nExiting!")
    exit()


#-----[global fariables]-----#
try:
    nm = nmap.PortScanner()
except:
    print("Nmap is not installed or accessible.\n Exting!")
    exit()
config = ConfigParser()    
dt_string = "%d/%m/%Y %H:%M:%S"


#-----[nmap scan]-----#
def nmap_custom_scan(filterd_devices_ip):
    config.read('config.ini')
    scan_file = config.get("write_to_file", "nmap-scan_file")
    arguments = config.get("command_line_arguments", "nmap_arguments")
    print(f"starting nmap at {datetime.now().strftime(dt_string)} using commandline arguments {arguments}")
    for ip in filterd_devices_ip:
        with open(scan_file, "a") as file:
            file.write(f"{ip['ip']}\n")
        print(f"Host: {ip['ip']}")
        nm.scan(ip['ip'], arguments=arguments)
        for host in nm.all_hosts():           
            for proto in nm[host].all_protocols():
                print("\tProtocol:", proto)
                ports = nm[host][proto].keys()
                for port in ports:
                    port_string = f"\tPort: {port}\t State: {nm[host][proto][port]['state']}\t Service: {nm[host][proto][port]['name']}"
                    print(port_string)
                    with open(scan_file, "a") as file:
                        file.write(f"\t{port_string}\n")
        print("\n")
    print(f"scan completen!\nSaved to {scan_file}")


# what happends if command arguments not right?
# nmap.nmap.PortScannerError: "nmap: option requires an argument -- 'p'\nSee the output of nmap -h for a summary of options.\n"