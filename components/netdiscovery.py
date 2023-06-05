#------------[Imports]------------#
try:
    from scapy.all import ARP, Ether, srp
    from mac_vendor_lookup import MacLookup, BaseMacLookup
    import netifaces as ni
    from configparser import ConfigParser 
except ModuleNotFoundError as e:
    print(f"Netdiscovery. {e}.\nExiting!")
    exit()
      
   #-----[local variables]-----#
config = ConfigParser()


#-----[network discovery class]-----#
class NetDiscovery():

    #-----[Get current network]-----#
    def get_current_network(self):
        config.read('config.ini')
        interface = config.get("netdiscovery", "interface") 
        try:
            default_interface = ni.gateways()[interface][ni.AF_INET][1]
        
        except:
            print(f"{interface} is not found. Using default interface.") 
            default_interface = ni.gateways()['default'][ni.AF_INET][1]

        ipadres = ni.ifaddresses(default_interface)[ni.AF_INET][0]['addr']
        netmask = ni.ifaddresses(default_interface)[ni.AF_INET][0]['netmask']
        
        dot_decimaal = ipadres.split(".")
        del dot_decimaal[3]
        dot_decimaal.append("0")
        ipadres = ".".join(dot_decimaal) 

        binary_mask = ''.join(format(int(x), '08b') for x in netmask.split('.'))
        cidr = str(len(binary_mask.rstrip('0')))
        
        default_network = ipadres+"/"+cidr
        return default_network


    #-----[Network discovery]-----#
    def discover_devices(self):
        ip_range = self.get_current_network() 
        print("Discovering network...")
        arp = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp
        
        result = srp(packet, timeout=3, verbose=0)[0]
        devices = []

        for send, received in result:
            try:
                BaseMacLookup.cache_path = "./mac-vendors.txt"
                vendor = MacLookup().lookup(received.hwsrc)

            except KeyError:
                vendor =  "Unknown"

            devices.append({'ip': received.psrc, 'mac': received.hwsrc, 'vendor': vendor})

        self.write_to_file(devices)
        return devices


    #-----[write to file]-----#
    def write_to_file(self, devices):
        
        config.read('config.ini')
        file_name = config.get("write_to_file", "devices_file")
        for device in devices:
            with open(file_name, "a") as file:
                file.write(f"IP: {device['ip']}\t MAC: {device['mac']}\t VENDOR: {device['vendor']}\n")
        print(f"Scan output saved to {file_name}")