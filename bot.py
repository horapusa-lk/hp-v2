import subprocess


class ServerManager:
    def gen_expire_date(self, valid_dates):
        """
        generate the config expire date
        :param valid_dates: how many days valid
        :return: expire date as string
        """
        from datetime import date, timedelta
        today = date.today()
        expire_date = today + timedelta(days=valid_dates)
        expire_date = str(expire_date)
        return expire_date

    def check_expired(self, expire_date):
        """
        :param expire_date: get expire date as string
        :return: expired or not as bool value
        """
        from datetime import datetime, date
        expire_date = str(expire_date)
        today = date.today()
        today = str(today)
        today = datetime.strptime(today, "%Y-%m-%d").date()
        expire_date = datetime.strptime(expire_date, "%Y-%m-%d").date()
        if expire_date <= today:
            return True
        else:
            return False

    def create_new_config(self, name, valid_dates):
        """ creates new vless config file
        :param name: user input as string
        :param valid_dates: vaild days required as int value
        :return: vless config as str
        """
        import uuid
        import requests
        import json
        from datetime import date
        public_ip = requests.get('https://api.ipify.org')
        public_ip = public_ip.text
        with open('/usr/local/etc/xray/config.json') as json_file:
            json_file = json.load(json_file)
        uuid = uuid.uuid4()
        today = date.today()
        today = str(today)
        expire_date = self.gen_expire_date(valid_dates)
        json_file["inbounds"][0]["settings"]["clients"].append({
            "id": f"{uuid}",
            "user_name": f"{name}",
            "created_date": f"{today}",
            "expire_date": f"{expire_date}"
        })
        vless_config = f"""vless://{uuid}@{public_ip}:443?security=xtls&encryption=none&headerType=none&type=tcp&flow=tls-rprx-direct&sni=zoom.us#{name}-Hora-Pusa-VPN"""
        with open('/usr/local/etc/xray/config.json', 'w') as json_write:
            json.dump(json_file, json_write)
        subprocess.run("sudo service xray restart", shell=True)
        return vless_config

    def delete_expired_config_files(self):
        """
        Delete expired vless configs
        """
        import json
        with open('/usr/local/etc/xray/config.json') as json_file:
            json_file = json.load(json_file)

        expired_user_index_list = []
        user_index_int = 0

        for user in json_file["inbounds"][0]["settings"]["clients"]:
            expire_date = user["expire_date"]
            if self.check_expired(expire_date):
                expired_user_index_list.append(user_index_int)
            user_index_int += 1

        for user_index in expired_user_index_list:
            del json_file["inbounds"][0]["settings"]["clients"][user_index]

        with open('/usr/local/etc/xray/config.json', 'w') as json_write:
            json.dump(json_file, json_write)
        subprocess.run("sudo service xray restart", shell=True)

    def delete_v2ray_config(self, config_index):
        """Delete the vless config
        :param config_index: config index as int
        """
        import json
        import subprocess
        config_index -= 1
        with open('/usr/local/etc/xray/config.json') as json_file:  # /usr/local/etc/xray/config.json
            json_file = json.load(json_file)
        del json_file["inbounds"][0]["settings"]["clients"][config_index]
        with open('/usr/local/etc/xray/config.json', 'w') as json_write:
            json.dump(json_file, json_write)
        subprocess.run("sudo service xray restart", shell=True)

    def list_all_v2ray_configs(self):
        """
        list all vless configs available in the server
        :return: vless configs as list
        """
        import requests
        import json
        public_ip = requests.get('https://api.ipify.org')
        public_ip = public_ip.text
        with open('/usr/local/etc/xray/config.json') as json_file:  # /usr/local/etc/xray/config.json
            json_file = json.load(json_file)
        config_list = []
        uuid_index = 0
        for i in json_file["inbounds"][0]["settings"]["clients"]:
            uuid = json_file["inbounds"][0]["settings"]["clients"][uuid_index]["id"]
            name = json_file["inbounds"][0]["settings"]["clients"][uuid_index]["user_name"]
            created_date = json_file["inbounds"][0]["settings"]["clients"][uuid_index]["created_date"]
            expire_date = json_file["inbounds"][0]["settings"]["clients"][uuid_index]["expire_date"]
            config_list.append(f"""Name : {name}
Created date : {created_date}    
Expire date : {expire_date}
Config text : vless://{uuid}@{public_ip}:443?security=xtls&encryption=none&headerType=none&type=tcp&flow=tls-rprx-direct&sni=zoom.us#{name}-Hora-Pusa-VPN""")

            uuid_index += 1
        return config_list


server_manager = ServerManager()
def pannel():
    print(f"""¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶11111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶11111111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
¶¶¶¶¶¶¶¶¶¶11111111111111111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
¶¶¶¶¶¶¶1111111111111111111111111¶¶¶¶¶¶¶¶¶¶¶¶¶
¶¶¶¶¶1111111¶¶¶¶¶¶¶¶111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
¶¶¶¶11111111¶¶¶111¶¶¶¶¶¶¶1111111¶¶¶¶¶¶¶¶¶¶¶¶¶
¶¶¶1111111111¶¶¶1111111111111111111¶¶¶¶¶¶¶¶¶¶
¶¶¶111111111111¶¶¶¶1111111111¶¶¶¶¶¶1¶¶¶¶¶1¶¶¶
¶¶111111111111111111111111111¶¶111111111111¶¶
¶¶111111111111111111111111111111111111111111¶
¶1111¶¶¶¶1111111111111111111111111111111111¶¶
¶11¶¶¶¶¶111111111111111111111111111¶¶¶¶¶¶11¶¶
¶1¶¶¶¶¶111111111111111111111111111¶¶¶¶¶¶¶¶¶¶¶
¶¶¶¶¶¶¶11111111111¶11111111111111¶¶¶¶¶¶¶¶¶¶¶¶
¶¶¶¶¶¶111111111111¶¶1111111111111¶¶¶¶¶¶¶¶1¶¶¶
¶¶¶¶¶¶1111111111111¶¶¶111111111111¶¶¶¶¶11¶¶¶¶
¶¶¶¶¶¶1111111¶¶¶11111¶¶¶¶111111111111111¶¶¶¶¶
¶¶¶¶¶¶11111¶¶¶¶¶11111111¶¶¶¶¶¶¶¶¶¶¶¶111¶¶¶¶¶¶
¶¶¶¶¶¶111¶¶¶¶¶¶¶11111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
¶¶¶¶¶¶¶1¶¶¶¶¶¶¶¶¶11111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶11¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶

Welcome to horapusa server manager.
1. Create new v2ray config.
2. Delete v2ray config.
3. List all v2ray configs.
4. Restart serever.
5. Exit""")
    try:
        server_manager.delete_expired_config_files()
    except:
        pass

    command = int(input("> "))
    if command == 1:
        name = input("Enter Name : ")
        valid_dates = int(input("Enter valid days : "))
        new_config = server_manager.create_new_config(name, valid_dates)
        print(new_config)
    elif command == 2:
        config_index = int(input("Enter the config number to delete : "))
        server_manager.delete_v2ray_config(config_index)
    elif command == 3:
        config_list = server_manager.list_all_v2ray_configs()
        config_int = 1
        for config in config_list:
            print(f"""Config {config_int}
{config}
""")
            config_int += 1
    elif command == 4:
        subprocess.run("sudo reboot", shell=True)
    elif command == 5:
        exit()


while True:
    pannel()
