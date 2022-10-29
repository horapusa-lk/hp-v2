#!/usr/bin/python3

import platform
from configs import BOT_TOKEN
from configs import SUDO_ID
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import psutil
import os
import requests


def unit(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def monitor():
    uname = platform.uname()
    cpufreq = psutil.cpu_freq()
    mem = psutil.virtual_memory()
    internet = psutil.net_io_counters()
    sys = uname.system
    core = psutil.cpu_count(logical=True)
    cpu_freq_mx = cpufreq.max
    mem_total = (int(mem.total)) / (1024 * 1024 * 1024)

    output = f"""
    {"=" * 20} SYSTEM Info {"=" * 20}
            System       - {sys}
            Total Cores  - {core} Cores
            Cpu Usage    - {psutil.cpu_percent()}%
            Max Cpu Freq - {cpu_freq_mx}MHZ
            Total Ram    - {round(mem_total)}GB
            Ram in Use   - {unit(mem.used)} | {mem.percent}%
    {"=" * 20} Internet {"=" * 24}        
            Data Sent    - {unit(internet.bytes_sent)}
            Data Receive - {unit(internet.bytes_recv)}

    """
    return output


###############################################################################################


r = requests.get('https://ip4.seeip.org')
public_ip = r.text

# with open("/root/bot/bot.token", "r") as token:
#     bot_token = token.read()
#     bot_token = str(bot_token)
sudo = SUDO_ID
bot_token = BOT_TOKEN
updater = Updater(bot_token, use_context=True)

class ServerManager:
    def gen_expire_date(self,valid_dates):
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
        vless_config = f"""vless://{uuid}@{public_ip}:443?security=xtls&encryption=none&headerType=none&type=tcp&flow=xtls-rprx-direct&sni=your.package.sni#{name}-Hora-Pusa-VPN"""
        with open('/usr/local/etc/xray/config.json', 'w') as json_write:
            json.dump(json_file, json_write)
        os.system("sudo service xray restart")
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
Config text : vless://{uuid}@{public_ip}:443?security=xtls&encryption=none&headerType=none&type=tcp&flow=xtls-rprx-direct&sni=your.package.sni#{name}-Hora-Pusa-VPN""")

            uuid_index += 1
        return config_list


server_manager = ServerManager()


def start(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        update.message.reply_text("""Hello sir, Welcome to the Hora_Pusa-server-manager-bot.
    Please write
    /help to see the commands available.""")


def help(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        update.message.reply_text("""Available Commands :-
        /speed_test - test server speed.
        /hardware_usage - check hardware usage.
        /new_config <name> <vaild dates> - create v2ray config.
        /config_list - show all v2ray configs.
        /delete_config <config index> - delete v2ray config.
        /reboot_server - reboot the server.""")


def new_config(update: Update, context: CallbackContext):
    command = update.message.text[12:]
    command = list(command.split(" "))
    command[1] = int(command[1])
    name = command[0]
    valid_dates = command[1]
    valid_dates = str(valid_dates)
    valid_dates = int(valid_dates)
    if update.message.chat.id == sudo:
        try:
            config = server_manager.create_new_config(name, valid_dates)
            update.message.reply_text(config)
        except Exception:
            update.message.reply_text("Faild to create v2ray config.")


def delete_config(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        config_index = update.message.text[14:]
        config_index = int(config_index)
        try:
            server_manager.delete_v2ray_config(config_index)
            update.message.reply_text(f"Succesfully deleted config {config_index}")
        except Exception:
            update.message.reply_text("Faild to delete v2ray config.")


def speed_test(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        try:
            import speedtest

            # If you want to test against a specific server
            # servers = [1234]

            threads = None
            # If you want to use a single threaded test
            # threads = 1

            s = speedtest.Speedtest()
            s.get_best_server()
            s.download(threads=threads)
            s.upload(threads=threads)
            s.results.share()

            results_dict = s.results.dict()
            print(results_dict["share"])
            update.message.chat.send_photo(results_dict["share"])

        except Exception:
            update.message.reply_text("speedtest faild.")


def unknown(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        update.message.reply_text(
            "Sorry '%s' is not a valid command" % update.message.text)


def reboot_server(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        try:
            update.message.reply_text("Rebooting...")
            os.system("reboot")
        except Exception:
            update.message.reply_text("Reboot faild.")


def config_list(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        try:
            configs_list = server_manager.list_all_v2ray_configs()
            try:
                server_manager.delete_expired_config_files()
            except:
                pass
            for config in configs_list:
                update.message.reply_text(config)
        except Exception:
            update.message.reply_text("Faild to get config list.")


def hardware_usage(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        try:
            sys_usage = monitor()
            update.message.reply_text(sys_usage)
        except Exception:
            update.message.reply_photo("faild to get hardware info.")


def unknown_text(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        update.message.reply_text(
            "Sorry I can't recognize you , you said '%s'" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('new_config', new_config))
updater.dispatcher.add_handler(CommandHandler('config_list', config_list))
updater.dispatcher.add_handler(CommandHandler('delete_config', delete_config))
updater.dispatcher.add_handler(CommandHandler('speed_test', speed_test))
updater.dispatcher.add_handler(CommandHandler('hardware_usage', hardware_usage))
updater.dispatcher.add_handler(CommandHandler('reboot_server', reboot_server))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    Filters.command, unknown))  # Filters out unknown commands

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
