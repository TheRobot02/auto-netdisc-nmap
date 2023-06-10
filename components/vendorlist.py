try:
    import asyncio
    from mac_vendor_lookup import  BaseMacLookup, AsyncMacLookup
    from aiohttp import ClientConnectorError
    from hashlib import md5
    import requests
except ModuleNotFoundError as e:
    print(f"vendorlist. {e}.\nExiting!")
    exit()


class VendorList():
    #-----{vendorlist update}-----#
    async def vendors_update(self):
        print("Updating vendorlist...")
        try:
            BaseMacLookup.cache_path = "./mac-vendors.txt"
            await AsyncMacLookup().update_vendors()
            print("Updating vendorlist successfull!")
        except ClientConnectorError as e:
            print(e)


    #-----{IEEE standards-oui check}-----#
    def check_IEEE(self):
        response = requests.get("https://standards-oui.ieee.org/oui/oui.txt/")
        response_txt = response.text

        md5_hash = md5(response_txt.encode('utf-8'))
        current_md5 = md5_hash.hexdigest()

        try:
            with open('standards-oui_md5', 'r') as file:
                previous_md5 = file.read()
        except:
            with open('standards-oui_md5', 'w+') as file:
                file.write(current_md5)
                previous_md5 = file.read()

        if current_md5 == previous_md5:
            print("No vendor list update found.")
        else:
            print("Vendorlist change found.")

            with open('standards-oui_md5', 'w') as file:
                file.write(current_md5)
            asyncio.run(self.vendors_update())
