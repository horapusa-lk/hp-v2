import json
import subprocess
import requests

public_ip = requests.get('https://api.ipify.org')
public_ip = public_ip.text


def create_new_config():
    import uuid
    with open('/usr/local/etc/xray/config.json') as json_file:  # /usr/local/etc/xray/config.json
        json_file = json.load(json_file)
    uuid = uuid.uuid4()
    json_file["inbounds"][0]["settings"]["clients"].append({"id": f"{uuid}"})
    vless_config = f"""vless://{uuid}@{public_ip}:443?security=tls&encryption=none&type=ws&sni=hora.pusa.vpn#Hora-Pusa-VPN"""
    with open('/usr/local/etc/xray/config.json', 'w') as json_write:
        json.dump(json_file, json_write)
    subprocess.run("sudo service xray restart", shell=True)
    return vless_config


def delete_v2ray_config(config_index):
    config_index -= 1
    with open('/usr/local/etc/xray/config.json') as json_file:  # /usr/local/etc/xray/config.json
        json_file = json.load(json_file)
    del json_file["inbounds"][0]["settings"]["clients"][config_index]
    with open('/usr/local/etc/xray/config.json', 'w') as json_write:
        json.dump(json_file, json_write)
    subprocess.run("sudo service xray restart", shell=True)


def list_all_v2ray_configs():
    with open('/usr/local/etc/xray/config.json') as json_file:  # /usr/local/etc/xray/config.json
        json_file = json.load(json_file)
    config_list = []
    uuid_index = 0
    for i in json_file["inbounds"][0]["settings"]["clients"]:
        uuid = json_file["inbounds"][0]["settings"]["clients"][uuid_index]["id"]
        config_list.append(f"vless://{uuid}@{public_ip}:443?security=tls&encryption=none&type=ws&sni=hora.pusa.vpn#Hora-Pusa-VPN")
        uuid_index += 1
    return config_list


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
    command = int(input("> "))
    if command == 1:
        new_config = create_new_config()
        print(new_config)
    elif command == 2:
        config_index = int(input("Enter the config number to delete : "))
        delete_v2ray_config(config_index)
    elif command == 3:
        config_list = list_all_v2ray_configs()
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
