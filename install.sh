cd ~
apt update
apt install git
apt install python3
apt install python3-pip
git clone https://github.com/horapusa-lk/hp-v2
cd hp-v2
chmod +x *
pip3 install -r requirements.txt

echo Enter a bot token :
read bot_token
echo BOT_TOKEN=""$bot_token"" > /usr/bin/configs.py

echo Enter your telegram user id :
read SUDO_ID
echo SUDO_ID=$SUDO_ID >> /root/configs.py

cp /root/configs.py /usr/bin/
cp bot.py /usr/bin/
cp bot.service /lib/systemd/system/
sudo systemctl enable bot.service
bash v2ray.sh


