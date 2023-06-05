#------------[Imports]------------#
try:
    from configparser import ConfigParser 
    import re
except ModuleNotFoundError as e:
    print(f"ip_filter. {e}.\nExiting!")
    exit()

#-----[local fariables]-----#
config = ConfigParser()
ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"  # Regular expression pattern for IP addresses
ip_addresses = []

#-----[ip filtering from filtered device output]-----#
def filter_ip_addresses():
    config.read('config.ini')
    device_file = config.get("write_to_file", "devices_file_filterd")
    with open(device_file, "r") as file1:
        while line := file1.readline():
            match = re.findall(ip_pattern, line, flags=re.IGNORECASE)
            ip_addresses.append(match)
    return ip_addresses
    #ip_file = config.get("write_to_file", "devices_file_ip_filterd")
    #with open(device_file, "r") as file1:
    #    while line := file1.readline():
    #        match = re.findall(ip_pattern, line, flags=re.IGNORECASE)
    #        with open(ip_file, "a") as file2:
    #            for ip in match:
    #                file2.write(f"{ip}\n")
    #print(f"Filtered ip-addresses output saved to {ip_file}")