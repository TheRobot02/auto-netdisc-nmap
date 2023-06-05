#------------[Imports]------------#
try:
    import asyncio
    from configparser import ConfigParser 
    from os import remove, path
    from components import Vendorlist
    
except ModuleNotFoundError as e:
    print(f"startup_check. {e}.\nExiting!")
    exit()


#-----[local variables]-----#
config = ConfigParser()
vlist = Vendorlist()


#-----[startup check class]-----#
class Startup_check():

    #-----[startup check]-----#
    def startup_list(self):
        if path.exists("config.ini") == False:
            self.config_file()
        if path.exists("mac-vendors.txt") == False:
            print("No vendorlist has been found. Creating new vendorlist!")
            vlist.check_IEEE()
        else:
            while True:
                update_check_prompt = input("Do you want to update the local vendor list? (y/n): ")
                if update_check_prompt == "y":
                    vlist.check_IEEE()
                    break
                elif update_check_prompt == "n":
                    break
                else:
                    print(f"{update_check_prompt} is a non-valid input.")
                    continue
        config.read("config.ini")
        file_location = config.get("write_to_file", "devices_file")
        if path.exists(file_location):
            remove(file_location)
        file_location = config.get("write_to_file", "devices_file_filterd")
        if path.exists(file_location):
            remove(file_location)
        file_location = config.get("write_to_file", "nmap-scan_file")
        if path.exists(file_location):
            remove(file_location)


    #-----[Config file]-----#
    def config_file(self):
        config.add_section("netdiscovery")
        config.set("netdiscovery", "interface", "default")
        config.add_section("write_to_file")
        config.set("write_to_file", "devices_file", "devices.txt")
        config.set("write_to_file", "devices_file_filterd", "devices_filtered.txt")
        config.set("write_to_file", "devices_file_ip_filterd", "devices_ip_filtered.txt")
        config.set("write_to_file", "nmap-scan_file", "nmap-scan.txt")

        with open('config.ini', 'w') as config_file:
            config.write(config_file)
