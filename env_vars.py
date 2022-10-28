BOT_TOKEN = input("Enter your bot token : ")
SUDO_ID = input("Enter your telegram user id : ")
content = f'''
BOT_TOKEN = "{BOT_TOKEN}"
SUDO_ID = {SUDO_ID}
'''
with open("/usr/bin/configs.py", 'w') as env_vars:
    env_vars.write(content)
 
