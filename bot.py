#!/usr/bin/python3

import json
import platform
import subprocess
from configs import BOT_TOKEN
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

sudo = 1436625686

r = requests.get('https://ip4.seeip.org')
public_ip = r.text

# with open("/root/bot/bot.token", "r") as token:
#     bot_token = token.read()
#     bot_token = str(bot_token)

bot_token = BOT_TOKEN
updater = Updater(bot_token, use_context=True)


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
        config_list.append(
            f"vless://{uuid}@{public_ip}:443?security=xtls&encryption=none&headerType=none&type=tcp&flow=xtls-rprx-direct&sni=zoom.us#Hora-Pusa-XTLS")

        uuid_index += 1
    return config_list


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
        /new_config - create v2ray config.
        /config_list - show all v2ray configs.
        /delete_config <config index> - delete v2rat config.
        /reboot_server - reboot the server.""")


def new_config(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        try:
            config = create_new_config()
            update.message.reply_text(config)
        except Exception:
            update.message.reply_text("Faild to create v2ray config.")


def delete_config(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        config_index = update.message.text[14:]
        config_index = int(config_index)
        try:
            delete_v2ray_config(config_index)
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
