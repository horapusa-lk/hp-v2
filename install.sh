cd ~
apt update
apt install git
apt install python3
apt install python3-pip
git clone https://github.com/horapusa-lk/hp-v2
cd hp-v2
chmod +x *
pip3 install -r requirements.txt
cp configs.py /usr/bin/
cp bot.py /usr/bin/
cp bot.service /lib/systemd/system/
sudo systemctl enable test-py.service
bash v2ray.sh

echo Enter a bot token :
read bot_token
echo BOT_TOKEN=$bot_token > /root/configs.py
