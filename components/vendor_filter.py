#------------[Imports]------------#
try:
    from configparser import ConfigParser 
    import re
except ModuleNotFoundError as e:
    print(f"vendor_filter. {e}.\nExiting!")
    exit()


#-----[local variables]-----#
config = ConfigParser()
pattern = r"\bunknown\b"
filterd_vendors = []

 #-----[filter vendor from unknown]-----#
def filter_list(devices):
    try:
        config.read("config.ini")
        #file_name1 = config.get("write_to_file", "devices_file")
        file_name2 = config.get("write_to_file", "devices_file_filterd") #ERROR    configparser.NoOptionError: No option 'devices_file_filtered' in section: 'write_to_file'
        
        for device in devices:
            device_string = f"IP: {device['ip']}\t MAC: {device['mac']}\t VENDOR: {device['vendor']}"
            match = re.search(pattern, device_string, flags=re.IGNORECASE)
            if match == None:
                with open(file_name2, "a") as file2: # Hier ergens error
                    file2.write(f"IP: {device['ip']}\t MAC: {device['mac']}\t VENDOR: {device['vendor']}\n")
                filterd_vendors.append({'ip': device['ip']})
        print(f"Filtered vendors output saved to {file_name2}")
        return filterd_vendors 

    except FileNotFoundError as error:
        print(f"A error has occurred.\n{error}")