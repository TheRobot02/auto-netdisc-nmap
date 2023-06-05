try:
    from configparser import ConfigParser 
    from datetime import datetime
    import nmap
except ModuleNotFoundError as e:
    print(f"nmap_scan. {e}.\nExiting!")
    exit()


#-----[global fariables]-----#
config = ConfigParser()
nm = nmap.PortScanner()    
dt_string = "%d/%m/%Y %H:%M:%S"


#-----[nmap scan]-----#
def nmap_custom_scan(filterd_devices_ip):
    config.read('config.ini')
    scan_file = config.get("write_to_file", "nmap-scan_file")
    print(f"starting nmap at {datetime.now().strftime(dt_string)}")
    for ip in filterd_devices_ip:
        print(f"Host:, {ip['ip']}\n")
        nm.scan(ip['ip'], arguments=f'-vv -p-')
        for host in nm.all_hosts():           
            for proto in nm[host].all_protocols():
                print("Protocol:", proto)
                ports = nm[host][proto].keys()
                for port in ports:
                    port_string = f"Port: {port}\t State: {nm[host][proto][port]['state']}\t Service: {nm[host][proto][port]['name']}"
                    print(port_string)
                    with open(scan_file, "a") as file:
                        file.write(f"{port_string}\n")
    print(f"scan completen!\n Saved to {scan_file}")
